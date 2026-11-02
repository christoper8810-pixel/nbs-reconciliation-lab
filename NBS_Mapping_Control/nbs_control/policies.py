"""Versioned owner policies: reporting basis (effective date) and duplicate/subentry treatment.

Every save writes a new version and a history event; raw source dates and rows are never edited.
"""
from __future__ import annotations
import copy
import hashlib
import json
import uuid
from datetime import date
from pathlib import Path

from .rebuild_store import now

BASIS_FILE = 'reporting_basis_policies.json'
DUPLICATE_FILE = 'duplicate_policy.json'
TREATMENTS = ('UNRESOLVED_RETAIN_ALL', 'RETAIN_ALL_CONFIRMED_SUBENTRIES', 'COUNT_ONCE')


class ReportingBasisError(ValueError):
    pass


def _load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def doc_hash(doc) -> str:
    return hashlib.sha256(json.dumps(doc, sort_keys=True).encode()).hexdigest()


def _save(path, doc, before, actor, reason, kind):
    if not str(actor).strip() or not str(reason).strip():
        raise ValueError('Enter your name and a reason')
    path = Path(path)
    doc['version'] = int((before or {}).get('version', 0)) + 1
    doc['updated_at'] = now()
    doc['updated_by'] = actor
    doc['reason'] = reason
    history = path.parent / 'policy_history'
    history.mkdir(exist_ok=True)
    (history / f'{kind}-v{doc["version"]}-{uuid.uuid4().hex[:6]}.json').write_text(
        json.dumps({'at': doc['updated_at'], 'actor': actor, 'reason': reason, 'before': before, 'after': doc}, indent=1), encoding='utf-8')
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(doc, indent=1) + '\n', encoding='utf-8')
    tmp.replace(path)
    return doc


def ensure_basis_policy(config_dir, confirmation_path=None):
    path = Path(config_dir) / BASIS_FILE
    if path.exists():
        return _load(path)
    policies = []
    if confirmation_path and Path(confirmation_path).exists():
        conf = _load(confirmation_path)
        policies.append({
            'policy_id': 'CATEG-2026-09-30-OWNER',
            'dataset': conf['source']['dataset'],
            'source_sha256': conf['source']['sha256'],
            'filename': conf['source']['filename'],
            'raw_booking_date': conf['raw_booking_date'],
            'raw_processing_date': conf['raw_processing_date'],
            'effective_reporting_date': conf['effective_reporting_date'],
            'enabled': conf.get('enabled_for_implementation') is True,
            'status': conf['status'],
            'authority': conf['authority'] + ' (' + conf['recorded_date'] + '); reconfirmed by owner in the rebuild instruction',
            'owner_statement': conf['owner_statement'],
            'evidence': str(Path(confirmation_path).as_posix()),
            'scope': 'This exact source hash only; never applied to other uploads',
            'not_established': conf['not_established_by_this_confirmation'],
        })
    doc = {'schema_version': 1, 'version': 0, 'policies': policies}
    return _save(path, doc, None, 'system (from owner confirmation file)', 'Initial owner-confirmed basis policy', 'basis')


def save_basis_policy(config_dir, doc, actor, reason):
    path = Path(config_dir) / BASIS_FILE
    before = _load(path) if path.exists() else None
    for p in doc.get('policies', []):
        for f in ('policy_id', 'dataset', 'source_sha256', 'effective_reporting_date', 'raw_booking_date'):
            if not p.get(f):
                raise ValueError(f'Policy field {f} is required')
        date.fromisoformat(p['effective_reporting_date'])
        if not isinstance(p.get('enabled'), bool):
            raise ValueError('enabled must be true or false')
    return _save(path, copy.deepcopy(doc), before, actor, reason, 'basis')


def resolve_effective_date(policy_doc, dataset, source_sha256, booking_dates, processing_dates, report_date):
    """Effective reporting date for a source in a run, or a specific error.

    A source-hash-scoped owner policy wins; otherwise the source's single raw booking date must equal
    the report date. Mixed raw booking dates without a policy are rejected.
    """
    booking_dates = set(booking_dates)
    processing_dates = set(processing_dates)
    for p in policy_doc.get('policies', []):
        if p['dataset'] == dataset and p['source_sha256'] == source_sha256:
            if not p['enabled']:
                raise ReportingBasisError(f'Reporting-basis policy {p["policy_id"]} for this source is disabled')
            if booking_dates != {p['raw_booking_date']} or processing_dates != {p.get('raw_processing_date', p['raw_booking_date'])}:
                raise ReportingBasisError(f'Source raw dates {sorted(booking_dates)} / {sorted(processing_dates)} do not match policy {p["policy_id"]}')
            if p['effective_reporting_date'] != report_date:
                raise ReportingBasisError(f'Policy {p["policy_id"]} gives effective date {p["effective_reporting_date"]}, not run date {report_date}')
            return {'effective_reporting_date': p['effective_reporting_date'], 'basis': 'OWNER_CONFIRMED_SOURCE_POLICY',
                    'policy_id': p['policy_id'], 'policy_version': policy_doc.get('version'), 'authority': p['authority'],
                    'raw_booking_dates': sorted(booking_dates), 'raw_processing_dates': sorted(processing_dates)}
    if len(booking_dates) != 1:
        raise ReportingBasisError(f'{dataset} source mixes booking dates {sorted(booking_dates)[:5]}; no effective-date policy covers it')
    only = next(iter(booking_dates))
    if only != report_date:
        raise ReportingBasisError(f'{dataset} source is booked {only}; it is not a {report_date} source and no owner policy covers hash {source_sha256[:12]}')
    return {'effective_reporting_date': only, 'basis': 'RAW_BOOKING_DATE', 'policy_id': None, 'policy_version': policy_doc.get('version'),
            'raw_booking_dates': sorted(booking_dates), 'raw_processing_dates': sorted(processing_dates)}


def ensure_duplicate_policy(config_dir):
    path = Path(config_dir) / DUPLICATE_FILE
    if path.exists():
        return _load(path)
    doc = {'schema_version': 1, 'version': 0,
           'default_treatment': 'UNRESOLVED_RETAIN_ALL',
           'treatments': {
               'UNRESOLVED_RETAIN_ALL': 'Every exported row counts; repeated groups are reported as unresolved sensitivity',
               'RETAIN_ALL_CONFIRMED_SUBENTRIES': 'Owner/evidence confirms the identical rows are separate subentries',
               'COUNT_ONCE': 'Owner/evidence confirms identical rows are export duplicates; excess rows are excluded with reason'},
           'decisions': {},
           'note': 'Decisions are keyed by value fingerprint, never by row position. No row is deleted.'}
    return _save(path, doc, None, 'system', 'Initial provisional duplicate policy (no deduplication)', 'duplicates')


def save_duplicate_policy(config_dir, doc, actor, reason):
    if doc.get('default_treatment') not in TREATMENTS:
        raise ValueError('Unknown default treatment')
    for fp, d in doc.get('decisions', {}).items():
        if d.get('treatment') not in TREATMENTS:
            raise ValueError(f'Unknown treatment for {fp[:12]}')
    path = Path(config_dir) / DUPLICATE_FILE
    before = _load(path) if path.exists() else None
    return _save(path, copy.deepcopy(doc), before, actor, reason, 'duplicates')


def duplicate_treatment(doc, fingerprint):
    d = doc.get('decisions', {}).get(fingerprint)
    return d['treatment'] if d else doc['default_treatment']


def row_weights(conn, source_sha256, doc):
    """{row_no: (counted 0/1, state)} for every row. Within a COUNT_ONCE group the lowest row is counted;
    identical rows have identical amounts so the amount effect is order-independent."""
    weights = {}
    groups = {}
    for row_no, fp in conn.execute('SELECT row_no, fingerprint FROM categ_events WHERE source_sha256=?', (source_sha256,)):
        groups.setdefault(fp, []).append(row_no)
    for fp, rows in groups.items():
        rows.sort()
        if len(rows) == 1:
            weights[rows[0]] = (1, 'UNIQUE_OBSERVATION')
            continue
        t = duplicate_treatment(doc, fp)
        for i, r in enumerate(rows):
            if t == 'COUNT_ONCE':
                weights[r] = (1, 'COUNT_ONCE_KEPT') if i == 0 else (0, 'EXCLUDED_DUPLICATE_EXPORT')
            elif t == 'RETAIN_ALL_CONFIRMED_SUBENTRIES':
                weights[r] = (1, 'CONFIRMED_SUBENTRY')
            else:
                weights[r] = (1, 'UNRESOLVED_REPEAT')
    return weights

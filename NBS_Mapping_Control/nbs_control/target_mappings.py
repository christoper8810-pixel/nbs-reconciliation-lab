"""Code-keyed NBS target catalogue and versioned, owner-editable target mappings.

Target identity is BO table code + full QCB item code (never a worksheet row). Measures are
identified by validated header name with their semantic definition from the measure catalogue.
The 1,037 exact-path matches are DRAFT candidates only; the 611 unmatched items form the review
queue. Nothing is activated by import.
"""
from __future__ import annotations
import copy
import csv
import hashlib
import json
import re
import uuid
from pathlib import Path

from .rebuild_store import now
from .categ_data import FILTER_FIELDS as CATEG_FIELDS

MAPPING_FILE = 'target_mappings.json'
STATUSES = ('UNRESOLVED', 'DRAFT_CANDIDATE', 'PROVISIONAL', 'APPROVED', 'NOT_APPLICABLE', 'DISABLED')
METHODS = ('NONE', 'LEGACY_RULE', 'CATEG_EVENTS', 'SUBTOTAL_OF_CHILDREN', 'QCB_COMPOSITION', 'QCB_POPULATION', 'SOURCE_RULE')
# Table layouts for population propagation; other tables have measure sets the stock facts cannot split.
TABLE_LAYOUT = {'010': 'maturity_loan', '024': 'maturity_deposit', '012': 'size', '025': 'size', '011': 'risk',
                '044': 'sector_columns', '045': 'sector_columns'}
GEO_TABLES = {'001', '002', '006', '008', '009', '014', '015', '019', '021', '023', '026', '027', '029', '031', '034', '035', '036', '039', '100', '200', '300'}
CALCULATING = ('DRAFT_CANDIDATE', 'PROVISIONAL', 'APPROVED')
OPS = {'eq', 'in', 'prefix', 'not_blank', 'blank'}
DATE_BASES = ('STOCK_AS_OF', 'EVENTS_EFFECTIVE_PERIOD', 'NOT_DEFINED')
GEOGRAPHY = ('UNKNOWN', 'IN', 'OUT')


def target_id(table, item):
    return f'{table}|{item}'


def _hash(doc):
    return hashlib.sha256(json.dumps(doc, sort_keys=True).encode()).hexdigest()


def validate_filter(node, fields=CATEG_FIELDS, depth=0):
    """Typed filter tree. Only known fields and operators; values are literal strings. No SQL."""
    if node is None:
        return
    if depth > 12:
        raise ValueError('Filter is nested too deeply')
    if not isinstance(node, dict):
        raise ValueError('Filter nodes must be objects')
    if 'all' in node or 'any' in node:
        key = 'all' if 'all' in node else 'any'
        if set(node) != {key} or not isinstance(node[key], list) or not node[key]:
            raise ValueError(f'{key} needs a non-empty list')
        for x in node[key]:
            validate_filter(x, fields, depth + 1)
        return
    if 'not' in node:
        if set(node) != {'not'}:
            raise ValueError('not takes one filter')
        validate_filter(node['not'], fields, depth + 1)
        return
    if set(node) - {'field', 'op', 'values'}:
        raise ValueError('Unknown filter keys')
    if node.get('field') not in fields:
        raise ValueError(f'Field {node.get("field")!r} is not allowed for this source (allowed: {", ".join(sorted(fields))})')
    if node.get('op') not in OPS:
        raise ValueError(f'Operator {node.get("op")!r} is not allowed')
    vals = node.get('values', [])
    if node['op'] in ('eq', 'in', 'prefix') and (not isinstance(vals, list) or not vals or not all(isinstance(v, str) and v for v in vals)):
        raise ValueError('Filter values must be a non-empty list of text values')


def compile_filter(node, params):
    """Typed tree -> parameterized SQL fragment over categ_events. Field names come from the whitelist."""
    if node is None:
        return '1'
    if 'all' in node:
        return '(' + ' AND '.join(compile_filter(x, params) for x in node['all']) + ')'
    if 'any' in node:
        return '(' + ' OR '.join(compile_filter(x, params) for x in node['any']) + ')'
    if 'not' in node:
        return '(NOT ' + compile_filter(node['not'], params) + ')'
    f = node['field']
    assert f in CATEG_FIELDS
    if node['op'] == 'blank':
        return f'({f} IS NULL)'
    if node['op'] == 'not_blank':
        return f'({f} IS NOT NULL)'
    if node['op'] == 'prefix':
        parts = []
        for v in node['values']:
            params.extend([len(v), v])
            parts.append(f"(substr(COALESCE({f},''),1,?)=?)")
        return '(' + ' OR '.join(parts) + ')'
    params.extend(node['values'])
    return f'({f} IN (' + ','.join('?' * len(node['values'])) + '))'


def validate_target(t, catalogue):
    if t.get('status') not in STATUSES:
        raise ValueError('Unknown mapping status')
    if t.get('method') not in METHODS:
        raise ValueError('Unknown calculation method')
    if t['method'] == 'LEGACY_RULE' and not t.get('legacy_rule_id'):
        raise ValueError('Choose the legacy calculation rule ID')
    if t['method'] == 'QCB_COMPOSITION' and not t.get('qcb_composition'):
        raise ValueError('A QCB composition needs at least one validated QCB rule per measure')
    if t['method'] == 'SOURCE_RULE':
        from .report_mapping import validate_spec
        if not t.get('parts'):
            raise ValueError('Add at least one source part in the logic builder')
        for i, p in enumerate(t['parts'], start=1):
            if p.get('kind') == 'CATEG':
                validate_filter(p.get('filter'))
                if p.get('filter') is None:
                    raise ValueError(f'Part {i}: choose the category entries (all events is never implicit)')
            else:
                validate_spec({'source': p.get('source'), 'measure': p.get('measure', 'components'), 'components': list(p.get('components') or []),
                               'filter': p.get('filter'), 'factor': p.get('factor', 1), 'enabled': True})
                if p.get('measure', 'components') == 'components' and p.get('source') != 'TB' and not p.get('components'):
                    raise ValueError(f'Part {i}: choose at least one balance type')
    if t['method'] == 'QCB_POPULATION' and (not t.get('legacy_rule_ids') or not t.get('qcb_rule_id')):
        raise ValueError('A QCB population mapping needs the source rule IDs and the QCB rule that equates them')
    if t['method'] == 'CATEG_EVENTS':
        cat = t.get('categ') or {}
        validate_filter(cat.get('filter'))
        if cat.get('filter') is None:
            raise ValueError('A category-event mapping needs a population filter (all events is never implicit)')
        if cat.get('sign') not in (1, -1):
            raise ValueError('Sign must be 1 or -1')
        if cat.get('geography', 'UNKNOWN') not in GEOGRAPHY:
            raise ValueError('Unknown geography basis')
    if t.get('date_basis', 'NOT_DEFINED') not in DATE_BASES:
        raise ValueError('Unknown date basis')
    measures = catalogue['tables'].get(t['table'], {}).get('measures', {})
    for name, ov in (t.get('overrides') or {}).items():
        if name not in measures:
            raise ValueError(f'Override measure {name!r} is not a header of table {t["table"]}')
        if not isinstance(ov, dict) or 'value' not in ov or not str(ov.get('reason', '')).strip():
            raise ValueError('An override needs a value and a reason')
        if ov['value'] is not None:
            from .money import parse_decimal
            parse_decimal(ov['value'])


def initial_mappings(store, ref_version, candidates_csv, catalogue):
    """Draft every BO item: exact-path candidates as DRAFT_CANDIDATE, others UNRESOLVED."""
    cands = {}
    if candidates_csv and Path(candidates_csv).exists():
        with open(candidates_csv, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                cands[target_id(r['table'], r['bo_item_code'])] = r
    targets = {}
    for table, item, desc, parent in store.execute(
            'SELECT table_code, item_code, description, parent_code FROM bo_items WHERE ref_version=? ORDER BY table_code, item_code', (ref_version,)):
        tid = target_id(table, item)
        c = cands.get(tid, {})
        ids = [x for x in (c.get('candidate_ids') or '').split('|') if x]
        single = len(ids) == 1 and c.get('status') == 'UNREVIEWED_EXACT_PATH_CANDIDATE'
        targets[tid] = {
            'target_id': tid, 'table': table, 'item_code': item, 'description': desc, 'parent_code': parent,
            'status': 'DRAFT_CANDIDATE' if single else 'UNRESOLVED',
            'method': 'LEGACY_RULE' if single else 'NONE',
            'legacy_rule_id': ids[0] if single else None, 'candidate_ids': ids,
            'candidate_basis': c.get('status') or 'NO_CANDIDATE',
            'categ': None, 'overrides': {}, 'date_basis': 'STOCK_AS_OF' if single else 'NOT_DEFINED',
            'effective_from': None, 'effective_to': None,
            'evidence': ('Exact normalized hierarchy path match to earlier mapping row ' + c.get('candidate_old_rows', '') +
                         '; unreviewed, not an approved account mapping') if single else
                        ('Multiple candidates; review required' if len(ids) > 1 else 'No candidate; in review queue'),
            'author': 'system draft', 'reason': 'Initial draft crosswalk from 17 Oct 2026 review',
        }
    special = [{'target_id': f'{t}|SPECIAL', 'table': t, 'schema': json.loads(f)}
               for t, f in store.execute('SELECT table_code, fields FROM bo_special WHERE ref_version=?', (ref_version,))]
    for s in special:
        targets[s['target_id']] = {'target_id': s['target_id'], 'table': s['table'], 'item_code': 'SPECIAL', 'description':
                                   'Table-020 acquisition schema (Acquistion No, Provision Amount, Net Value)', 'parent_code': None,
                                   'status': 'UNRESOLVED', 'method': 'NONE', 'legacy_rule_id': None, 'candidate_ids': [],
                                   'candidate_basis': 'SPECIAL_SCHEMA', 'categ': None, 'overrides': {}, 'date_basis': 'NOT_DEFINED',
                                   'effective_from': None, 'effective_to': None,
                                   'evidence': 'Acquisition feed not supplied', 'author': 'system draft', 'reason': 'Special schema retained'}
    return {'schema_version': 1, 'version': 1, 'reference_version': ref_version, 'created_at': now(),
            'targets': targets, 'exclusive_partitions': []}


def ensure(config_dir, store, ref_version, candidates_csv, catalogue):
    path = Path(config_dir) / MAPPING_FILE
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    doc = initial_mappings(store, ref_version, candidates_csv, catalogue)
    _write(path, doc, None, 'system', 'Initial draft crosswalk')
    return doc


def load(config_dir):
    return json.loads((Path(config_dir) / MAPPING_FILE).read_text(encoding='utf-8'))


def _write(path, doc, before_target, actor, reason, tid=None):
    path = Path(path)
    versions = path.parent / 'mapping_versions'
    versions.mkdir(exist_ok=True)
    snapshot = versions / f'target_mappings-v{doc["version"]:05d}.json'
    snapshot.write_text(json.dumps(doc, indent=0, sort_keys=True), encoding='utf-8')
    event = {'at': now(), 'actor': actor, 'reason': reason, 'version': doc['version'], 'target_id': tid,
             'before': before_target, 'after': doc['targets'].get(tid) if tid else None, 'snapshot': snapshot.name}
    with (versions / 'history.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(event) + '\n')
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(doc, indent=0, sort_keys=True) + '\n', encoding='utf-8')
    tmp.replace(path)


def save_target(config_dir, tid, updated, actor, reason, catalogue):
    if not str(actor).strip() or not str(reason).strip():
        raise ValueError('Enter your name and a reason for the change')
    path = Path(config_dir) / MAPPING_FILE
    doc = json.loads(path.read_text(encoding='utf-8'))
    if tid not in doc['targets']:
        raise ValueError('Unknown target')
    old = doc['targets'][tid]
    for f in ('target_id', 'table', 'item_code'):
        if updated.get(f) != old.get(f):
            raise ValueError(f'{f} identifies the target and cannot be changed')
    validate_target(updated, catalogue)
    if updated == old:
        raise ValueError('No change to save')
    new = copy.deepcopy(doc)
    updated = dict(updated, author=actor, reason=reason, changed_at=now())
    new['targets'][tid] = updated
    new['version'] = doc['version'] + 1
    _write(path, new, old, actor, reason, tid)
    return new


def history(config_dir, tid=None):
    p = Path(config_dir) / 'mapping_versions' / 'history.jsonl'
    if not p.exists():
        return []
    out = [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
    return [e for e in out if tid is None or e.get('target_id') == tid]


def mapping_hash(doc):
    return _hash(doc)


def check_disjoint_codes(codes):
    """Reject a subtotal input set that contains both a parent and any of its descendants."""
    codes = list(codes)
    for a in codes:
        for b in codes:
            if a != b and b.startswith(a):
                raise ValueError(f'Cannot sum {a} together with its descendant {b}: the parent already contains it')
    return codes


def save_batch(config_dir, updates, actor, reason, catalogue):
    """Apply many target updates as one new mapping version with one history event per target."""
    if not str(actor).strip() or not str(reason).strip():
        raise ValueError('Enter your name and a reason for the change')
    path = Path(config_dir) / MAPPING_FILE
    doc = json.loads(path.read_text(encoding='utf-8'))
    new = copy.deepcopy(doc)
    changed = []
    for tid, upd in updates.items():
        old = doc['targets'][tid]
        for f in ('target_id', 'table', 'item_code'):
            if upd.get(f) != old.get(f):
                raise ValueError(f'{tid}: {f} cannot change')
        validate_target(upd, catalogue)
        if upd != old:
            new['targets'][tid] = dict(upd, author=upd.get('author') if is_system(upd) else actor, reason=reason, changed_at=now())
            changed.append((tid, old))
    if not changed:
        return doc, 0
    new['version'] = doc['version'] + 1
    _write(path, new, None, actor, reason)
    with (path.parent / 'mapping_versions' / 'history.jsonl').open('a', encoding='utf-8') as f:
        for tid, old in changed:
            f.write(json.dumps({'at': now(), 'actor': actor, 'reason': reason, 'version': new['version'], 'target_id': tid,
                                'before': old, 'after': new['targets'][tid]}) + '\n')
    return new, len(changed)


def is_system(t):
    return t.get('author') in ('system draft', 'system: structural crosswalk', 'system: QCB validation rules', 'system: selector distinctness check', 'system: evidence-based drafting', 'system: hierarchy subtotal')


def reset_derived(doc):
    """Return QCB-derived and withheld system drafts to their structural-crosswalk state before re-deriving."""
    out = {}
    for tid, t in doc['targets'].items():
        if t.get('author') in ('system: QCB validation rules', 'system: selector distinctness check', 'system: hierarchy subtotal'):
            base = {k: v for k, v in t.items() if k not in ('qcb_composition', 'legacy_rule_ids', 'qcb_rule_id', 'qcb_code', 'layout', 'suggested_legacy_rule_id')}
            m = t.get('structural_link')
            if m and m['basis'] == 'STRUCTURAL_CODE_TEXT_CONFIRMED':
                base.update(status='DRAFT_CANDIDATE', method='LEGACY_RULE', legacy_rule_id=m['rule_id'], candidate_basis=m['basis'],
                            evidence=f'QCB code structure matches legacy row {m["row"]} "{m["path"][-80:]}" (text score {m["text_score"]}); unreviewed')
            else:
                base.update(status='UNRESOLVED', method='NONE', candidate_basis='NO_CANDIDATE', evidence='No candidate; in review queue')
            out[tid] = dict(base, author='system: structural crosswalk')
    return out


def upgrade_from_evidence(doc, links, qcb_rules, rules, catalogue):
    """Propose mappings for system-drafted targets only (owner edits are never overwritten).

    1. Structural code crosswalk confirmed by text  -> LEGACY_RULE draft.
       Structural match with a different label       -> stays UNRESOLVED with the suggestion recorded.
    2. QCB '=' rule defining the target from other targets with the same measures -> QCB_COMPOSITION draft.
    3. QCB '=' rule equating the target's whole population with mapped targets in another breakdown
       -> QCB_POPULATION draft (same accounts, this table's layout).
    """
    from . import qcb_validations as q
    targets = doc['targets']
    updates = {}

    def calculable(tid, ts):
        t = ts.get(tid)
        if not t or t['status'] not in CALCULATING:
            return False
        if t['method'] == 'LEGACY_RULE':
            s = rules.get(t.get('legacy_rule_id') or '')
            return bool(s and s.get('enabled') and s.get('source'))
        return t['method'] in ('QCB_COMPOSITION', 'QCB_POPULATION', 'CATEG_EVENTS', 'SOURCE_RULE')

    for tid, t in targets.items():
        if not is_system(t) or t['item_code'] == 'SPECIAL':
            continue
        link = links.get(t['item_code'])
        if not link:
            continue
        m = link[0]
        u = dict(t, structural_link=m)
        if m['basis'] == 'STRUCTURAL_CODE_TEXT_CONFIRMED':
            if t['method'] == 'LEGACY_RULE' and t.get('legacy_rule_id') == m['rule_id']:
                if not t['evidence'].startswith('QCB code structure') and 'Structural code match confirms' not in t['evidence']:
                    u['evidence'] = t['evidence'] + f' | Structural code match confirms rule {m["rule_id"]} (row {m["row"]})'
            elif t['status'] == 'UNRESOLVED':
                u.update(status='DRAFT_CANDIDATE', method='LEGACY_RULE', legacy_rule_id=m['rule_id'], candidate_ids=[m['rule_id']],
                         candidate_basis=m['basis'], date_basis='STOCK_AS_OF',
                         evidence=f'QCB code structure matches legacy row {m["row"]} "{m["path"][-80:]}" (text score {m["text_score"]}); unreviewed')
        else:
            u.update(suggested_legacy_rule_id=m['rule_id'],
                     evidence=f'Code structure points to legacy row {m["row"]} but the label differs '
                              f'("{t["description"]}" vs "{m["path"].split(" > ")[-1].strip(". ")}"); definition review needed')
        if u != t:
            updates[tid] = dict(u, author='system: structural crosswalk')
    work = dict(targets, **updates)
    def full_population(table, measures):
        """True when the measures add up to the whole population of the table row (not one column of it)."""
        tm_ = catalogue['tables'].get(table, {}).get('measures', {})
        primary = {m['semantic'] for m in tm_.values() if m.get('primary', True) and m['kind'] == 'money' and not m.get('subtotal')}
        sems = {q.semantic_for(table, x) or (tm_.get(q.header_for(table, x, catalogue) or '', {}).get('semantic')) for x in measures}
        return bool(primary) and (sems >= primary or sems == {'TOTAL_LC', 'TOTAL_FC'} or sems == {'TOTAL'})
    # QCB rules: iterate so compositions can build on compositions.
    by_target = {}
    for r in qcb_rules:
        if r['operator'] != '=' or r['kind'].startswith('ADDITIONAL') or q.has_ratio(r['left_ast']) or q.has_ratio(r['right_ast']):
            continue
        for a, b in ((r['left_ast'], r['right_ast']), (r['right_ast'], r['left_ast'])):
            if a['t'] != 'term':
                continue
            bt = list(q.terms(b))
            if not bt or any(n['t'] == 'num' for _, n in (b.get('parts') or [])):
                continue
            by_target.setdefault(target_id(a['table'], a['item']), []).append((r, a, b, bt))
    for _ in range(6):
        added = 0
        for tid, cands in by_target.items():
            t = work.get(tid)
            if not t or not is_system(t) or calculable(tid, work):
                continue
            comp = dict(t.get('qcb_composition') or {})
            pop = None
            for r, a, b, bt in cands:
                others = [target_id(x['table'], x['item']) for x in bt]
                if tid in others or not all(calculable(o, work) for o in others):
                    continue
                if all(x['measures'] == a['measures'] for x in bt) and len(a['measures']) == 1:
                    comp.setdefault(a['measures'][0], {'rule_id': r['rule_id'], 'qcb_code': r['qcb_code'], 'kind': r['kind'], 'side': 'left' if a is r['left_ast'] else 'right'})
                elif (r['kind'] == 'CROSS_DIMENSION_SAME_POPULATION' and t['table'] in TABLE_LAYOUT | dict.fromkeys(GEO_TABLES, 'geo')
                      and full_population(a['table'], a['measures']) and all(full_population(x['table'], x['measures']) for x in bt)):
                    srcs = [work[o] for o in others]
                    if all(s['method'] == 'LEGACY_RULE' for s in srcs) and pop is None:
                        pop = {'legacy_rule_ids': [s['legacy_rule_id'] for s in srcs], 'qcb_rule_id': r['rule_id'], 'qcb_code': r['qcb_code']}
            if comp:
                work[tid] = dict(t, status='DRAFT_CANDIDATE', method='QCB_COMPOSITION', qcb_composition=comp, date_basis='STOCK_AS_OF',
                                 candidate_basis='QCB_VALIDATION_COMPOSITION', author='system: QCB validation rules',
                                 evidence='Defined by QCB validation rule(s) ' + ', '.join(sorted({v['qcb_code'] + ' (' + v['rule_id'] + ')' for v in comp.values()}))
                                          + ' from mapped targets; values pass those rules by construction')
                updates[tid] = work[tid]
                added += 1
            elif pop:
                work[tid] = dict(t, status='DRAFT_CANDIDATE', method='QCB_POPULATION', date_basis='STOCK_AS_OF',
                                 layout=TABLE_LAYOUT.get(t['table'], 'geo'), candidate_basis='QCB_VALIDATION_SAME_POPULATION',
                                 author='system: QCB validation rules', **pop,
                                 evidence=f'QCB rule {pop["qcb_code"]} ({pop["qcb_rule_id"]}) states this item equals the population of '
                                          + ', '.join(pop['legacy_rule_ids']) + '; same accounts in this table\'s breakdown')
                updates[tid] = work[tid]
                added += 1
        if not added:
            break
    return updates


def non_distinct_selectors(doc, rules, hierarchy_cfg):
    """Targets whose effective account selector (after inherited parent dimensions) is identical to a sibling's
    or to its parent's. Such drafts cannot separate their populations and would double count."""
    from .rebuild_engine import inherit_hierarchy
    sig = {}
    for tid, t in doc['targets'].items():
        if t['status'] not in CALCULATING or t['method'] != 'LEGACY_RULE':
            continue
        s = rules.get(t.get('legacy_rule_id') or '')
        if not s or not s.get('enabled') or not s.get('source'):
            continue
        eff, _ = inherit_hierarchy(s, hierarchy_cfg)
        sig[tid] = json.dumps([eff['source'], eff['measure'], eff.get('components'), eff.get('filter'), eff.get('negative_filter'), eff['factor']], sort_keys=True)
    empty = {k for k, s in sig.items() if 'NONE_CONVENTIONAL_PRODUCT' in s}  # deliberately empty lines are all zero, not duplicates
    groups = {}
    for tid, t in doc['targets'].items():
        if tid in sig and t.get('parent_code'):
            groups.setdefault(f'{t["table"]}|{t["parent_code"]}', []).append(tid)
    flagged = {}
    for parent, kids in groups.items():
        by_sig = {}
        for k in kids:
            by_sig.setdefault(sig[k], []).append(k)
        for same in by_sig.values():
            same = [k for k in same if k not in empty]
            if len(same) > 1:
                for k in same:
                    flagged[k] = 'same selector as sibling(s) ' + ', '.join(x.split('|')[1] for x in same if x != k)
        if parent in sig and len(kids) > 1:
            for k in kids:
                if all(o in empty for o in kids if o != k):
                    continue  # the only non-empty child legitimately equals its parent
                if sig[k] == sig[parent] and k not in flagged:
                    flagged[k] = 'same selector as its parent ' + parent.split('|')[1]
    # Any two items of one table that are not ancestor/descendant and share a selector would double count.
    by_table_sig = {}
    for tid, s in sig.items():
        by_table_sig.setdefault((doc['targets'][tid]['table'], s), []).append(tid)
    for (table, _), same in by_table_sig.items():
        same = [k for k in same if k not in empty]
        if len(same) < 2:
            continue
        codes = {k: doc['targets'][k]['item_code'] for k in same}
        for k in same:
            others = [o for o in same if o != k and not codes[o].startswith(codes[k]) and not codes[k].startswith(codes[o])]
            if others and k not in flagged:
                flagged[k] = 'same selector as non-nested item(s) ' + ', '.join(codes[o] for o in others[:4])
    return flagged


def propose_subtotals(doc, rules, catalogue, bo_values):
    """Parents without their own selector become SUBTOTAL_OF_CHILDREN drafts when every immediate child is
    calculable and the reference confirms the line is additive (parent = sum of children within rounding for every
    primary money column). Deepest levels first so subtotals can build on subtotals."""
    from decimal import Decimal
    targets = doc['targets']
    kids = {}
    for tid, t in targets.items():
        if t.get('parent_code'):
            kids.setdefault(f'{t["table"]}|{t["parent_code"]}', []).append(tid)

    def calculable(tid):
        t = targets[tid]
        if t['status'] not in CALCULATING:
            return False
        if t['method'] == 'LEGACY_RULE':
            s = rules.get(t.get('legacy_rule_id') or '')
            return bool(s and s.get('enabled') and s.get('source'))
        return t['method'] in ('QCB_COMPOSITION', 'QCB_POPULATION', 'CATEG_EVENTS', 'SUBTOTAL_OF_CHILDREN', 'SOURCE_RULE')

    updates = {}
    for tid in sorted(kids, key=lambda k: -len(k)):
        t = targets.get(tid)
        if not t or not is_system(t) or calculable(tid) or not all(calculable(k) for k in kids[tid]):
            continue
        measures = {h: m for h, m in catalogue['tables'][t['table']]['measures'].items() if m['kind'] == 'money' and m.get('primary', True)}
        additive, checked = True, 0
        for h in measures:
            pv = bo_values.get((t['table'], t['item_code'], h))
            cv = [bo_values.get((t['table'], targets[k]['item_code'], h)) for k in kids[tid]]
            if pv is None or any(v is None for v in cv):
                continue
            checked += 1
            if abs(Decimal(pv) - sum(Decimal(v) for v in cv)) > Decimal(500000) * (len(cv) + 1):  # 0.5 display unit each, in 1e-6 units
                additive = False
                break
        if not additive or not checked:
            continue
        t2 = dict(t, status='DRAFT_CANDIDATE', method='SUBTOTAL_OF_CHILDREN', candidate_basis='HIERARCHY_SUBTOTAL_REFERENCE_ADDITIVE',
                  author='system: hierarchy subtotal', date_basis='STOCK_AS_OF',
                  evidence=f'No own selector; sum of its {len(kids[tid])} immediate items. The reference confirms this line is additive '
                           f'(parent = sum of children within rounding in {checked} money columns).')
        targets[tid] = t2
        updates[tid] = t2
    return updates

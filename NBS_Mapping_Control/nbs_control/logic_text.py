"""Plain-language description of each NBS line's logic: source, accounts, exact balance types, split.

Used by the NBS report screen, the Balance types page and the stakeholder export, so everyone sees the same words.
"""
from __future__ import annotations
import json
from pathlib import Path

from .mapping_export import readable
from .rebuild_engine import correct_components, inherit_hierarchy

SOURCE_WORDS = {'ECB': 'ECB balances', 'ECB_LOAN': 'ECB balances of loan accounts', 'ECB_DEPOSIT': 'ECB balances of deposit accounts',
                'TB': 'Ethix trial balance'}
SPLIT_WORDS = {'geo': 'Inside/Outside Qatar (residency) and LC/FC (currency)', 'tb': 'LC/FC only (the GL has no residency)',
               'maturity_loan': 'remaining maturity (month-end bands)', 'maturity_deposit': 'current & call / saving / time-deposit maturity',
               'size': 'amount bands per customer', 'risk': 'credit risk grade', 'sector_columns': 'economic sector and LC/FC'}


class Context:
    def __init__(self, root):
        from . import rebuild_run as rr
        p = rr.Paths(root)
        self.rules = json.loads(p.rules.read_text(encoding='utf-8'))['rules']
        self.settings = rr.run_settings(p)
        self.balance = json.loads((p.config / 'balance_rules.json').read_text(encoding='utf-8'))
        self.policies = json.loads((p.config / 'report_product_policies.json').read_text(encoding='utf-8')).get('products', {})
        self.available = set()
        if p.bank.exists():
            from .bank_data import load_manifest
            self.available = set(load_manifest(p.bank)['ECB']['component_columns'])


def _signed(types, sign, available):
    out = []
    for t in types:
        out.append({'type': t, 'sign': sign, 'in_extract': (t in available) if available else None})
    return out


def balance_types(spec, ctx):
    """Explicit balance types (with sign) a stock rule adds up, per product where policies differ.
    Returns [{'scope': str, 'types': [{'type','sign','in_extract'}], 'extra': [str]}]."""
    m = spec.get('measure')
    g = ctx.balance['groups']
    f = spec.get('factor', 1)
    neg = -1 * f
    if m == 'components':
        return [{'scope': 'all selected accounts', 'types': _signed(spec.get('components') or [], f, ctx.available), 'extra': []}]
    if m == 'deposit':
        return [{'scope': 'deposit accounts', 'types': _signed(['CREDIT', 'CURACCOUNT'], f, ctx.available), 'extra': []}]
    if m == 'amount':
        return [{'scope': 'trial balance' if spec.get('source') == 'TB' else 'source amount', 'types': [],
                 'extra': ['Equivalent balance (Equiv Cur Bal) of the selected GL accounts' if spec.get('source') == 'TB' else 'Amount field of the source file']}]
    if m == 'outstanding':
        return [{'scope': 'loan accounts', 'types': _signed(g['OUTSTANDING'], neg, ctx.available), 'extra': []}]
    if m == 'earned':
        return [{'scope': 'loan accounts', 'types': _signed(g['AMORTIZED_EARNED'], neg, ctx.available), 'extra': []}]
    if m == 'unearned':
        return [{'scope': 'loan accounts', 'types': _signed(g['UNEARNED_PROFIT'], neg, ctx.available), 'extra': []}]
    if m in ('carrying', 'ethix_carrying'):
        base = {'scope': 'loan accounts' + (' (all products except ' + ', '.join(sorted(k for k, v in ctx.policies.items() if v.get('enabled'))) + ')'
                                            if m == 'ethix_carrying' and ctx.policies else ''),
                'types': _signed(g['OUTSTANDING'] + g['AMORTIZED_EARNED'], neg, ctx.available),
                'extra': ['+ Ethix loan fees (Loan_Fees_QAR from the loan file; not a T24 balance type)']}
        out = [base]
        if m == 'ethix_carrying':
            for prod, pol in sorted(ctx.policies.items()):
                if not pol.get('enabled'):
                    continue
                types = [{'type': t, 'sign': c * f, 'in_extract': (t in ctx.available) if ctx.available else None} for t, c in pol['parent_coefficients'].items()]
                extra = ['+ Ethix loan fees'] if pol.get('add_ethix_fees') else []
                if pol.get('linked_coefficients'):
                    extra.append('+ linked current account (CLS, category 6050): ' + ', '.join(f'{"-" if c < 0 else "+"}{t}' for t, c in pol['linked_coefficients'].items()))
                out.append({'scope': f'{prod} loans (product policy)', 'types': types, 'extra': extra})
        return out
    return [{'scope': 'not defined', 'types': [], 'extra': [f'measure {m}']}]


def types_text(blocks):
    lines = []
    for b in blocks:
        t = ' '.join(f'{"-" if x["sign"] < 0 else "+"}{x["type"]}{"*" if x["in_extract"] is False else ""}' for x in b['types'])
        lines.append(f'{b["scope"]}: {t} {" ".join(b["extra"])}'.strip())
    return '\n'.join(lines)


def describe(t, ctx, results=None):
    """{'how', 'source', 'accounts', 'types' (blocks), 'split', 'status_words'} for one NBS target."""
    out = {'how': '', 'source': '', 'accounts': '', 'types': [], 'split': '', 'inherited': ''}
    meth = t['method']
    specs = []
    if meth == 'LEGACY_RULE':
        s = ctx.rules.get(t.get('legacy_rule_id') or '')
        if s and s.get('source'):
            specs = [s]
        elif s:
            out['how'] = f'Not calculated yet: report-layout row {s.get("row")} has no executable source rule. Check the original Temenos cells in the mapping review.'
            return out
    elif meth == 'QCB_POPULATION':
        specs = [ctx.rules[x] for x in t.get('legacy_rule_ids') or [] if x in ctx.rules]
        out['how'] = f'Same accounts as the items QCB rule {t.get("qcb_code")} equates it with'
    elif meth == 'SOURCE_RULE':
        for p in t.get('parts') or []:
            if p.get('kind') == 'CATEG':
                out['types'].append({'scope': p.get('label') or 'category entries', 'types': [], 'extra': ['category entries where ' + readable(p.get('filter'))]})
            else:
                specs.append(dict(p, path='', notes=[]))
        out['how'] = 'Built in the logic builder'
    elif meth == 'QCB_COMPOSITION':
        out['how'] = 'Sum of other NBS items, as QCB validation rule(s) ' + ', '.join(sorted({v['qcb_code'] for v in (t.get('qcb_composition') or {}).values()})) + ' define it'
        return out
    elif meth == 'SUBTOTAL_OF_CHILDREN':
        out['how'] = 'Sum of its sub-items'
        return out
    elif meth == 'CATEG_EVENTS':
        out['how'] = 'Category entries where ' + readable((t.get('categ') or {}).get('filter'))
        return out
    else:
        out['how'] = 'Not mapped yet' + (': ' + t.get('evidence', '') if t.get('evidence') else '')
        return out
    accounts, inherited, srcs, layouts = [], [], [], []
    for s in specs:
        s2, fixes = correct_components(s, ctx.settings.get('component_corrections'))
        e, notes = inherit_hierarchy(s2, ctx.settings.get('hierarchy_predicates'))
        srcs.append(SOURCE_WORDS.get(e['source'], e['source']))
        accounts.append(readable(e.get('filter')))
        inherited += fixes + notes
        out['types'] += balance_types(e, ctx)
        layouts.append(t.get('layout') if meth == 'QCB_POPULATION' else ('tb' if e['source'] == 'TB' else e.get('layout') or 'geo'))
    out['source'] = ' + '.join(dict.fromkeys(srcs))
    out['accounts'] = ' | '.join(accounts)
    out['inherited'] = '; '.join(dict.fromkeys(inherited))
    out['split'] = ', '.join(dict.fromkeys(SPLIT_WORDS.get(x, x or '') for x in layouts))
    if not out['how']:
        if specs:
            evidence = specs[0].get('evidence', '')
            out['how'] = ('Temenos source: ' + evidence[4:] if evidence.startswith('T24 ') else
                          'Engine draft linked to Ehab report-layout row ' + str(specs[0].get('row')))
    return out

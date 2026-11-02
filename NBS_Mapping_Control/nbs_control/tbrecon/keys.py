"""Configurable CONSOL_KEY layouts (AC/PRODUCT_S3 and PL are different layouts).

Every segment carries a 'verified' flag and its evidence. Unverified positions are used, but each
run reports them, and the misalignment diagnostic tests them against data. Parsed keys are cached.
"""
from __future__ import annotations


class KeyLayout:
    def __init__(self, name, spec):
        self.name = name
        self.prefix = spec.get('prefix')
        self.sep = spec.get('separator', '.')
        self.min_tokens = int(spec.get('min_tokens', 1))
        self.segments = {k: int(v['position']) for k, v in spec['segments'].items()}
        self.verified = {k: bool(v.get('verified')) for k, v in spec['segments'].items()}
        self.evidence = {k: v.get('evidence', '') for k, v in spec['segments'].items()}
        self._cache = {}

    @property
    def dimensions(self):
        return list(self.segments)

    def unverified(self):
        return [k for k, v in self.verified.items() if not v]

    def parse(self, key):
        """Return (dims, tokens, error). dims values are '' when the segment is empty."""
        key = '' if key is None else str(key).strip()
        hit = self._cache.get(key)
        if hit is not None:
            return hit
        if not key:
            res = ({}, [], 'EMPTY_KEY')
        else:
            tokens = key.split(self.sep)
            if self.prefix and tokens[0] != self.prefix:
                res = ({}, tokens, f'PREFIX_{tokens[0] or "BLANK"}_NOT_{self.prefix}')
            elif len(tokens) < self.min_tokens:
                res = ({}, tokens, f'TOO_FEW_TOKENS_{len(tokens)}_LT_{self.min_tokens}')
            else:
                dims = {}
                for d, pos in self.segments.items():
                    dims[d] = tokens[pos].strip().upper() if -len(tokens) <= pos < len(tokens) else ''
                res = (dims, tokens, None)
        if len(self._cache) < 2_000_000:
            self._cache[key] = res
        return res

    def token_at(self, tokens, pos):
        return tokens[pos].strip().upper() if -len(tokens) <= pos < len(tokens) else ''

    def describe(self):
        return {d: {'position': p, 'verified': self.verified[d], 'evidence': self.evidence[d]} for d, p in self.segments.items()}


def layouts(cfg):
    return {name: KeyLayout(name, spec) for name, spec in cfg['consol_key_layouts'].items()}

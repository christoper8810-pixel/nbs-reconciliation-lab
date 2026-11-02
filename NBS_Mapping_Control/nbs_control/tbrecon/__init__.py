"""Whole trial-balance migration reconciliation (tbrecon).

Three independent streams are reconstructed from source data and authorised mappings and are
combined only at the controlled final aggregation:

* Engine A - PRODUCT_S3 / asset-type balances: CONSOL_KEY + atomic balance type -> GL rule -> target GL.
* Engine B - INTERNAL_CUS_ACC: one-to-one account mapping. Never uses CONSOL_KEY.
* Engine C - PL: its own configurable PL key layout and PL rules.

A fourth, explicitly labelled DIRECT stream maps legacy TB lines that no account-level population
covers through the legacy GL mapping, and only when that mapping has exactly one target.

Nothing here connects to a bank, executes workbook text, plugs a difference or alters an approved
mapping. Missing inputs make the affected analysis SOURCE_PENDING / INCOMPLETE, never reconciled.
"""

ENGINE_VERSION = 'tbrecon-1.0.0'

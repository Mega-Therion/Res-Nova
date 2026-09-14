#!/usr/bin/env python3
"""Schema + exact-term check on the mu_std certificate.

Complements verify_mu_std.py: that script PROVES the identities and emits the
certificate; this one asserts the emitted certificate still carries every
required field and the exact series terms, so a silent shape change is caught.
P_math only -- neither script says anything about the action-level derivation.
"""
from __future__ import annotations

import json
from pathlib import Path

# Resolved from this file, not a sandbox-absolute path (the original hard-coded
# /home/ubuntu/wide-research/, which exists on no machine here).
path = Path(__file__).resolve().parent.parent / 'docs' / 'recovered' / 'mu_std_certificate.json'
data = json.loads(path.read_text(encoding='utf-8'))
required = {
    'definition', 'potential', 'F_derivative', 'rapidity_identity',
    'deep_series', 'newtonian_series', 'mu_derivative',
    'F_second_derivative', 'evidence_boundary'
}
assert set(data) == required, (set(data), required)
assert data['evidence_boundary'].startswith('P_math only')
assert 'x*mu_std' in data['F_derivative']
assert 'tanh' in data['rapidity_identity']
assert '3*x**5/8' in data['deep_series']
assert '-5*x**7/16' in data['deep_series']
assert '3/(8*x**4)' in data['newtonian_series']
assert '- 5/(16*x**6)' in data['newtonian_series']
print(f'PASS: certificate schema and exact series terms verified ({len(data)} fields)')

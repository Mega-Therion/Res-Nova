import re, sys, json, subprocess, pathlib
R = '/tmp/res-nova'
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
paths = [l for l in git('ls-tree', '-r', '--name-only', 'origin/main').splitlines() if l]
mods = {}
for p in paths:
    if p.endswith('.lean'):
        stem = pathlib.Path(p).stem
        mods.setdefault(stem, '')
        mods[stem] += git('show', 'origin/main:' + p)
def strip_comments(t):
    t = re.sub(r'/-.*?-/', '', t, flags=re.S)
    return re.sub(r'--[^\n]*', '', t)
thms = {m: set(re.findall(r"^(?:theorem|lemma)\s+([A-Za-z0-9_']+)", t, re.M)) for m, t in mods.items()}
sorries = {m: len(re.findall(r'\bsorry\b', strip_comments(t))) for m, t in mods.items()}
docs = [p for p in paths if p.endswith('.md') and not any(x in p for x in ('node_modules/', 'research-hub/client/', 'legacy/'))]
errs, checked, phantom = [], 0, False
for p in docs:
    txt = git('show', 'origin/main:' + p)
    for i, line in enumerate(txt.splitlines(), 1):
        if 'phantom' in line.lower():
            phantom = True
        if not line.strip():
            phantom = False
        if phantom:
            continue
        if '[P]' not in line:
            continue
        if any(w in line for w in ('Phantom','phantom','missing','Missing','Nowhere','Duplicate','Duplicates','Conflates','retired','planned')):
            continue
        checked += 1
        for m in re.findall(r'\b([A-Z][A-Za-z0-9_]+)\.lean\b', line):
            if m not in mods:
                errs.append(f'{p}:{i} cites missing {m}.lean')
            elif sorries.get(m, 0):
                errs.append(f'{p}:{i} cites {m}.lean with {sorries[m]} sorry')
        for mod, th in re.findall(r'\b([A-Z][A-Za-z0-9_]+)\.([a-z][A-Za-z0-9_\']*)\b', line):
            if th in ('lean', 'md', 'json', 'tex', 'py'):
                continue
            if mod in thms and th not in thms[mod]:
                errs.append(f'{p}:{i} cites {mod}.{th} not found in kernel source')
print(json.dumps({'lean_modules': len(mods), 'docs_scanned': len(docs), 'checked_P_lines': checked, 'errors': len(errs), 'detail': errs[:30]}, indent=1))
sys.exit(1 if errs else 0)

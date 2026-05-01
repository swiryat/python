import pathlib, re
root = pathlib.Path('.').resolve()
py_files = [p for p in root.iterdir() if p.is_file() and p.suffix == '.py']
normalize = lambda name: re.sub(r'\s*\(\d+\)|\s*-\s*\d+$|\s*\(copy\)|\s*\(.*?\)$', '', name, flags=re.IGNORECASE).strip().lower()
by_norm = {}
for p in py_files:
    n = normalize(p.stem)
    by_norm.setdefault(n, []).append(p.name)
for k,v in sorted(by_norm.items(), key=lambda x:(-len(x[1]), x[0]))[:40]:
    if len(v) > 1:
        print(k, len(v), v)
print('--- total py files', len(py_files))

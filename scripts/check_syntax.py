import py_compile
from pathlib import Path

root = Path(r'C:\Users\swer\github\swiryat-python')
errors = []
for p in sorted(root.rglob('*.py')):
    if '__pycache__' in p.parts:
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as e:
        errors.append((p.relative_to(root), e))

print(f'checked {sum(1 for p in root.rglob("*.py") if "__pycache__" not in p.parts)} files')
print(f'errors {len(errors)}')
for path, err in errors[:50]:
    print(path, err)
if len(errors) > 50:
    print('...plus', len(errors) - 50, 'more errors')

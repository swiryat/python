import shutil
from pathlib import Path

root = Path(r'C:\Users\swer\github\swiryat-python')
scripts_root = root / 'scripts'
archive = scripts_root / 'archive'
archive_duplicates = archive / 'duplicates'
archive_conflicts = archive / 'conflicts'
archive_duplicates.mkdir(parents=True, exist_ok=True)
archive_conflicts.mkdir(parents=True, exist_ok=True)

# Move duplicate files from scripts/duplicates to scripts/archive/duplicates
duplicates_dir = scripts_root / 'duplicates'
if duplicates_dir.exists():
    for item in duplicates_dir.iterdir():
        if item.name == '__pycache__':
            continue
        target = archive_duplicates / item.name
        if item.is_file():
            shutil.move(str(item), str(target))
        elif item.is_dir():
            shutil.move(str(item), str(archive_duplicates / item.name))

# Move files containing merge conflict markers into archive/conflicts preserving structure.
for p in sorted(scripts_root.rglob('*.py')):
    if 'archive' in p.parts:
        continue
    try:
        text = p.read_text(errors='ignore')
    except Exception:
        continue
    if '<<<<<<<' in text or '>>>>>>>' in text or '=======' in text:
        rel = p.relative_to(scripts_root)
        target = archive_conflicts / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(target))

# Move project files with conflict markers into archive/conflicts/projects preserving projects path
for p in sorted((scripts_root / 'projects').rglob('*.py')):
    if 'archive' in p.parts:
        continue
    try:
        text = p.read_text(errors='ignore')
    except Exception:
        continue
    if '<<<<<<<' in text or '>>>>>>>' in text or '=======' in text:
        rel = p.relative_to(scripts_root)
        target = archive_conflicts / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(target))

# Remove empty directories under scripts and scripts/projects after moving files.
def remove_empty_dirs(path: Path):
    for child in sorted(path.iterdir(), reverse=True):
        if child.is_dir():
            remove_empty_dirs(child)
            try:
                child.rmdir()
            except OSError:
                pass

remove_empty_dirs(scripts_root / 'projects')
remove_empty_dirs(duplicates_dir)
print('archive cleanup complete')

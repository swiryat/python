# swiryat-python repository cleanup

Organized content for easier inspection and repair.

## Structure

- `scripts/` — main Python script collection.
- `scripts/duplicates/` — duplicate/versioned copies and special backups.
- `scripts/projects/` — grouped sub-project folders extracted from the repository root.
- `assets/` — miscellaneous data files, assets, and external modules.
- `education/` — Python notebooks for advanced learning, data science and task practice.

## Notes

- Project folders such as `loto`, `myapp`, `parser`, `radio`, `raspoznavatel`, `алгоритмы`, `база данных`, and task collections are now under `scripts/projects/`.
- External add-on `MB-Lab-1_7_8` was moved into `assets/`.
- A syntax scan found Python syntax issues in several files, including duplicate files and task collections with merge conflict markers.
- The `scripts/check_syntax.py` tool can be used to rerun syntax validation.

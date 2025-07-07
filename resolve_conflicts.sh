#!/bin/bash

echo "🔍 Поиск конфликтов..."

conflict_files=$(git diff --name-only --diff-filter=U)

if [ -z "$conflict_files" ]; then
  echo "✅ Нет файлов с конфликтами."
  exit 0
fi

for file in $conflict_files; do
  # Проверим, файл ли это (а не папка)
  if [ -f "$file" ]; then
    echo "⚙ Обработка: $file"
    
    # Создаём временный файл безопасно
    tmpfile=$(mktemp)
    
    # Удаляем конфликтные маркеры, оставляя только текущую версию (ours)
    awk '
      BEGIN {skip=0}
      /^<{7}/ {skip=1; next}
      /^={7}/ {skip=2; next}
      /^>{7}/ {skip=0; next}
      skip==1 {next}
      skip==0 {print}
    ' "$file" > "$tmpfile"

    mv "$tmpfile" "$file"
  else
    echo "⛔ Пропущено (не файл): $file"
  fi
done

echo "🟢 Завершено. Выполни:"
echo "    git add ."
echo "    git commit -m 'Auto-resolve conflicts (ours strategy)'"

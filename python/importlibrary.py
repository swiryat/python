import os

# Укажите путь к папке site-packages
site_packages_path = r"G:\Users\swer\AppData\Local\Programs\Python\Python312\Lib\site-packages"  # Замените на ваш путь

# Список модулей и версий
modules_with_versions = []

# Проход по файлам и папкам
for item in os.listdir(site_packages_path):
    if item.endswith(".dist-info"):
        metadata_path = os.path.join(site_packages_path, item, "METADATA")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("Name:"):
                        module_name = line.split(":")[1].strip()
                    if line.startswith("Version:"):
                        version = line.split(":")[1].strip()
                        modules_with_versions.append(f"{module_name}=={version}")
                        break

# Сохраняем список модулей с версиями в файл
with open("modules_with_versions.txt", "w") as file:
    for module in sorted(set(modules_with_versions)):  # Убираем дубли и сортируем
        file.write(module + "\n")

print("Список модулей с версиями сохранён в файле modules_with_versions.txt")

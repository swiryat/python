import json
import re
from typing import List, Optional, Union
from packaging import version  # pip install packaging

# Загрузка правил из JSON-файла
def load_vuln_rules(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Семантическое сравнение версий
def is_version_less(v1: str, v2: str) -> bool:
    try:
        return version.parse(v1) < version.parse(v2)
    except:
        # В случае ошибок парсинга – считаем неуязвимым
        return False

# Универсальная функция проверки уязвимостей
def check_vulnerabilities(port: int, banner: Optional[str], vuln_rules: List[dict]) -> List[str]:
    if not banner:
        return []

    results = []
    for rule in vuln_rules:
        # Поддержка wildcard - если ports = ["*"], правило для всех портов
        if ("ports" in rule and 
            (port in rule["ports"] or "*" in rule["ports"])):

            pattern = rule.get("pattern")
            if pattern:
                match = re.search(pattern, banner, re.IGNORECASE)
                if match:
                    found_version = match.group(1)
                    if is_version_less(found_version, rule["min_version"]):
                        results.append(rule["description"].format(version=found_version))
    return results

# Пример использования
if __name__ == "__main__":
    rules = load_vuln_rules("vuln_rules.json")

    sample_banner = "SSH-2.6.1p1 Ubuntu-4ubuntu0.3"
    port = 22

    vulns = check_vulnerabilities(port, sample_banner, rules)
    print("Найденные уязвимости:", vulns)

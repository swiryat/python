# Скрипт для расчета дозировок при ацетальдегидной интоксикации

def calc_thiamine(severity):
    """Расчет дозировки тиамина (витамин B1)"""
    if severity == "легкая":
        return 100
    elif severity == "средняя":
        return 200
    elif severity == "тяжелая":
        return 400
    else:
        return 100  # default

def calc_nac(weight_kg):
    """Расчет схемы введения АЦЦ (ацетилцистеина)"""
    loading_dose = 150 * weight_kg  # мг
    maintenance_4h = 50 * weight_kg  # мг
    maintenance_16h = 100 * weight_kg  # мг
    return loading_dose, maintenance_4h, maintenance_16h

def calc_glutathione(severity):
    """Расчет дозировки глутатиона"""
    if severity == "легкая":
        return 600
    elif severity == "средняя":
        return 1200
    elif severity == "тяжелая":
        return 1800
    else:
        return 600

def generate_protocol(weight_kg, severity):
    print(f"\n📋 Протокол лечения ацетальдегидной интоксикации для пациента {weight_kg} кг ({severity} степень):\n")

    # Тиамин
    thiamine_dose = calc_thiamine(severity)
    print(f"🔹 Тиамин (B1): {thiamine_dose} мг в/в, 1–3 раза в сутки.")
    print("    ➤ Вводить капельно или медленно болюсно. Важен до введения глюкозы!")

    # АЦЦ (ацетилцистеин)
    nac_load, nac_maint_4h, nac_maint_16h = calc_nac(weight_kg)
    print(f"\n🔹 Ацетилцистеин (АЦЦ):")
    print(f"    ➤ Загрузка: {nac_load:.0f} мг (150 мг/кг) в/в за 15 минут.")
    print(f"    ➤ Поддержка 4 ч: {nac_maint_4h:.0f} мг (50 мг/кг).")
    print(f"    ➤ Поддержка 16 ч: {nac_maint_16h:.0f} мг (100 мг/кг).")

    # Глутатион
    glut_dose = calc_glutathione(severity)
    print(f"\n🔹 Глутатион: {glut_dose} мг в/в или в/м, 1–2 раза в сутки.")
    print("    ➤ Вводить медленно, можно комбинировать с АЦЦ.")

    # Общие рекомендации
    print(f"\n🩺 Рекомендуется:")
    print("    • Пульсоксиметрия и мониторинг давления каждые 30 мин.")
    print("    • Контроль АЛТ/АСТ, креатинина, электролитов.")
    print("    • При рвоте: метоклопрамид 10 мг в/в.")
    print("    • Госпитализация в отделение интенсивной терапии — обязательна при тяжелом состоянии.")

# --- Главная функция ---
def main():
    print("💊 Калькулятор протокола экстренной терапии при ацетальдегидной интоксикации")

    try:
        weight_kg = float(input("Введите массу тела пациента (в кг): "))
        print("Укажите степень тяжести интоксикации: легкая / средняя / тяжелая")
        severity = input("Степень: ").strip().lower()

        generate_protocol(weight_kg, severity)

    except ValueError:
        print("❗ Ошибка: введите корректное число для массы тела.")

# --- Запуск ---
if __name__ == "__main__":
    main()

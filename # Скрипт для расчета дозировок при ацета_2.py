import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import time

# --- Логика расчётов дозировок ---
def calc_thiamine(severity):
    if severity == "легкая":
        return 100
    elif severity == "средняя":
        return 200
    elif severity == "тяжелая":
        return 400
    return 100

def calc_nac(weight_kg):
    return 150 * weight_kg, 50 * weight_kg, 100 * weight_kg

def calc_glutathione(severity):
    if severity == "легкая":
        return 600
    elif severity == "средняя":
        return 1200
    elif severity == "тяжелая":
        return 1800
    return 600

def generate_protocol(weight_kg, severity):
    thiamine_dose = calc_thiamine(severity)
    nac_load, nac_maint_4h, nac_maint_16h = calc_nac(weight_kg)
    glut_dose = calc_glutathione(severity)

    protocol = f"""
📋 Протокол лечения ацетальдегидной интоксикации для пациента {weight_kg} кг ({severity} степень):

🔹 Тиамин (B1): {thiamine_dose} мг в/в, 1–3 раза в сутки.
    ➤ Вводить капельно или медленно болюсно. Важен до введения глюкозы!

🔹 Ацетилцистеин (АЦЦ):
    ➤ Загрузка: {nac_load:.0f} мг (150 мг/кг) в/в за 15 минут.
    ➤ Поддержка 4 ч: {nac_maint_4h:.0f} мг (50 мг/кг).
    ➤ Поддержка 16 ч: {nac_maint_16h:.0f} мг (100 мг/кг).

🔹 Глутатион: {glut_dose} мг в/в или в/м, 1–2 раза в сутки.
    ➤ Вводить медленно, можно комбинировать с АЦЦ.

🩺 Рекомендуется:
    • Пульсоксиметрия и мониторинг давления каждые 30 мин.
    • Контроль АЛТ/АСТ, креатинина, электролитов.
    • При рвоте: метоклопрамид 10 мг в/в.
    • Госпитализация в ОИТ — обязательна при тяжелом состоянии.
"""
    return protocol.strip()

def save_to_pdf(text, filename="protocol_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(f"/mnt/data/{filename}")

# --- GUI интерфейс ---
def calculate_and_display():
    try:
        weight = float(entry_weight.get())
        severity = severity_var.get().lower()

        start_time = time.time()
        protocol = generate_protocol(weight, severity)
        duration = time.time() - start_time

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, protocol + f"\n\n⏱ Расчёт выполнен за {duration:.4f} сек.")

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректный вес пациента.")

def export_pdf():
    text = text_output.get("1.0", tk.END)
    if not text.strip():
        messagebox.showerror("Ошибка", "Нет данных для сохранения.")
        return
    save_to_pdf(text)
    messagebox.showinfo("Успешно", "Протокол сохранён в файл protocol_output.pdf")

# --- Основное окно ---
root = tk.Tk()
root.title("Протокол ацетальдегидной интоксикации")

tk.Label(root, text="Масса тела пациента (кг):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Степень тяжести:").pack()
severity_var = tk.StringVar(value="средняя")
tk.OptionMenu(root, severity_var, "легкая", "средняя", "тяжелая").pack()

tk.Button(root, text="Рассчитать протокол", command=calculate_and_display).pack(pady=5)
tk.Button(root, text="Сохранить в PDF", command=export_pdf).pack(pady=5)

text_output = tk.Text(root, height=25, width=90)
text_output.pack()

root.mainloop()


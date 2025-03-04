import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# 🔹 Названия сетевых адаптеров (замените, если у вас другие)
INTERFACES = ["Ethernet 3", "Ethernet 6"]

# 🔹 Пути к файлу hosts
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
BACKUP_PATH = r"C:\Windows\System32\drivers\etc\hosts_backup"

# 🔹 Список блокируемых сайтов
BLOCKED_SITES = [
    "www.google.com", "www.youtube.com", "www.yandex.ru",
    "www.mail.ru", "www.vk.com"
]

### 📌 ФУНКЦИИ ДЛЯ ОТКЛЮЧЕНИЯ/ВКЛЮЧЕНИЯ АДАПТЕРОВ ###
def disable_network():
    """ Отключает указанные сетевые адаптеры """
    try:
        for iface in INTERFACES:
            subprocess.run(f'netsh interface set interface name="{iface}" admin=disable', shell=True, check=True)
        messagebox.showinfo("Блокировка", "Интернет отключен!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")

def enable_network():
    """ Включает указанные сетевые адаптеры """
    try:
        for iface in INTERFACES:
            subprocess.run(f'netsh interface set interface name="{iface}" admin=enable', shell=True, check=True)
        messagebox.showinfo("Разблокировка", "Интернет включен!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")

### 📌 ФУНКЦИИ ДЛЯ БЛОКИРОВКИ/РАЗБЛОКИРОВКИ САЙТОВ ###
def block_websites():
    """ Блокирует сайты через hosts """
    try:
        if not os.path.exists(BACKUP_PATH):  # Делаем резервную копию
            with open(HOSTS_PATH, "r", encoding="ansi", errors="ignore") as original:
                with open(BACKUP_PATH, "w", encoding="utf-8") as backup:
                    backup.write(original.read())

        with open(HOSTS_PATH, "a", encoding="utf-8") as file:
            for site in BLOCKED_SITES:
                file.write(f"0.0.0.0 {site}\n")
        
        messagebox.showinfo("Блокировка", "Выбранные сайты заблокированы!")
    except PermissionError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")


def unblock_websites():
    """ Удаляет записи из hosts и разблокирует сайты """
    try:
        if os.path.exists(BACKUP_PATH):
            with open(BACKUP_PATH, "r", encoding="utf-8") as backup:
                with open(HOSTS_PATH, "w", encoding="utf-8") as original:
                    original.write(backup.read())
            os.remove(BACKUP_PATH)
            messagebox.showinfo("Разблокировка", "Выбранные сайты разблокированы!")
        else:
            messagebox.showwarning("Разблокировка", "Резервная копия не найдена, возможно, сайты уже разблокированы.")
    except PermissionError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")

### 📌 ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ###
root = tk.Tk()
root.title("Интернет Контроль")
root.geometry("350x250")

tk.Label(root, text="🔒 Управление интернетом", font=("Arial", 12)).pack(pady=5)

btn_disable_net = tk.Button(root, text="Отключить интернет", command=disable_network, bg="red", fg="white")
btn_disable_net.pack(pady=5)

btn_enable_net = tk.Button(root, text="Включить интернет", command=enable_network, bg="green", fg="white")
btn_enable_net.pack(pady=5)

tk.Label(root, text="🌐 Блокировка сайтов", font=("Arial", 12)).pack(pady=5)

btn_block_sites = tk.Button(root, text="Блокировать сайты (Google, VK, YouTube)", command=block_websites, bg="orange", fg="black")
btn_block_sites.pack(pady=5)

btn_unblock_sites = tk.Button(root, text="Разблокировать сайты", command=unblock_websites, bg="blue", fg="white")
btn_unblock_sites.pack(pady=5)

root.mainloop()

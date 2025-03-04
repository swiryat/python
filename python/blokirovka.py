import subprocess
import tkinter as tk
from tkinter import messagebox

# Названия активных сетевых интерфейсов (заменяем на ваши)
INTERFACES = ["Ethernet 3", "Ethernet 6"]

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

# Графический интерфейс
root = tk.Tk()
root.title("Интернет Блокер")
root.geometry("300x150")

btn_block = tk.Button(root, text="Отключить интернет", command=disable_network, bg="red", fg="white")
btn_block.pack(pady=10)

btn_unblock = tk.Button(root, text="Включить интернет", command=enable_network, bg="green", fg="white")
btn_unblock.pack(pady=10)

root.mainloop()

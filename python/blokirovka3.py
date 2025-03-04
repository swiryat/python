import subprocess
import tkinter as tk
from tkinter import messagebox
import socket

# Названия активных сетевых интерфейсов (замените на свои)
INTERFACES = ["Ethernet 3", "Ethernet 6"]
# Список сайтов для блокировки
BLOCKED_SITES = ["www.google.com", "www.youtube.com", "www.yandex.ru", "www.mail.ru", "www.vk.com"]

def get_ip(domain):
    """Получает IP-адрес по доменному имени"""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

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

def block_sites():
    """ Блокирует сайты через брандмауэр Windows """
    try:
        for site in BLOCKED_SITES:
            ip = get_ip(site)
            if ip:
                subprocess.run(f'powershell -Command "New-NetFirewallRule -DisplayName \"Block_{site}\" -Direction Outbound -Action Block -RemoteAddress {ip}"', shell=True, check=True)
        messagebox.showinfo("Блокировка сайтов", "Сайты заблокированы!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")

def unblock_sites():
    """ Разблокирует сайты через брандмауэр Windows """
    try:
        for site in BLOCKED_SITES:
            subprocess.run(f'powershell -Command "Remove-NetFirewallRule -DisplayName \"Block_{site}\""', shell=True, check=True)
        messagebox.showinfo("Разблокировка сайтов", "Сайты разблокированы!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Запустите программу от имени администратора!")

# Графический интерфейс
root = tk.Tk()
root.title("Интернет Блокер")
root.geometry("350x250")

tk.Label(root, text="Управление интернетом и сайтами", font=("Arial", 12)).pack(pady=10)

btn_block_net = tk.Button(root, text="Отключить интернет", command=disable_network, bg="red", fg="white", width=25)
btn_block_net.pack(pady=5)

btn_unblock_net = tk.Button(root, text="Включить интернет", command=enable_network, bg="green", fg="white", width=25)
btn_unblock_net.pack(pady=5)

btn_block_sites = tk.Button(root, text="Заблокировать сайты", command=block_sites, bg="orange", fg="black", width=25)
btn_block_sites.pack(pady=5)

btn_unblock_sites = tk.Button(root, text="Разблокировать сайты", command=unblock_sites, bg="blue", fg="white", width=25)
btn_unblock_sites.pack(pady=5)

root.mainloop()

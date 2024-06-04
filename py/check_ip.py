#!/usr/bin/python3

import socket
import subprocess

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def copy_to_clipboard(text):
    try:
        # Запускаем процесс xclip для копирования текста в буфер обмена
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
    except Exception as e:
        print(f"Не удалось сохранить в буфер обмена: {e}")

if __name__ == "__main__":
    ip_address = get_ip_address()
    copy_to_clipboard(ip_address)
    print(f"Ваш IP адрес: {ip_address} скопирован в буфер обмена.")
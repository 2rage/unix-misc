#!/usr/bin/python3

import socket
from check_ip import get_ip_address

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Таймаут ожидания попытки подключения
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Порт {port} на {host} открыт.")
        else:
            print(f"Порт {port} на {host} закрыт или не доступен.")
    except socket.error as e:
        print(f"Ошибка при проверке порта {port} на {host}: {e}")
    finally:
        sock.close()

def get_port_from_user():
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        port = input("Введите номер порта: ")
        try:
            port = int(port)
            if 1 <= port <= 65535:
                return port
            else:
                print("Номер порта должен быть в диапазоне от 1 до 65535")
        except ValueError:
                print("Введите корректное число")

        attempts += 1
        if attempts < max_attempts:
            print(f'Попытка {attempts} из {max_attempts}. Попробуйте снова.')
        else:
            print('Превышено количество попыток. Завершение программы')

if __name__ == "__main__":
    host = get_ip_address()  # Измените на IP или хостнейм, который нужно проверить
     
    port = get_port_from_user()
    if port is not None:
        check_port(host, port)
    else:
        print("Не удалось получить корректный номер порта.")
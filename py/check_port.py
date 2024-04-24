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

if __name__ == "__main__":
    host = get_ip_address()  # Измените на IP или хостнейм, который нужно проверить
    port = 7777
    check_port(host, port)
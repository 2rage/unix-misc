#!/usr/bin/env python3

import subprocess
import re

def hugo_server():

    cwd_path = '/home/the2rage/work/personal-site' # Путь к рабочей директории Hugo

    # Запускаем команду 'ip addr show eth0' и получаем вывод
    result = subprocess.run(['ip', 'addr', 'show', 'eth0'], stdout=subprocess.PIPE, text=True)
    
    # Ищем IP-адрес с помощью регулярных выражений
    ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
    if ip_match:
        wsl2_ipaddress = ip_match.group(1)
        # Запускаем сервер Hugo в указанной директории
        subprocess.run([
            'hugo', 'server',
            '--bind', wsl2_ipaddress,
            '--baseURL', f'http://{wsl2_ipaddress}',
            '-D', '-F', '--gc', '-w'
        ], cwd=cwd_path)
    return

# Вызываем функцию для запуска Hugo сервера
hugo_server()
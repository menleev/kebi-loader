import json
import os
import subprocess
import win32api, win32con, win32gui
import psutil
from zipfile import ZipFile
import time
import threading

drive = psutil.disk_partitions()[0].device

def menu():

    winv()

    os.system('cls')
    print('1. Обновить' '\033[35m ' 'Akebi''\033[0m')
    print('2. Обновить ' '\033[36m' 'Kebi''\033[0m')
    print('3. Обновить ' '\033[31m' 'Всё''\033[0m')
    print('\033[32m''Выберите пункт меню:''\033[0m')
    choice = input()

    if choice == '1':
        update_akebi()
        menu()

    elif choice == '2':
        update_kebi()
        menu()

    elif choice == '3':
        update_all()
        menu()
    else:
        print('Неверный пункт меню')
        menu()

def winv():
    if os.path.basename(os.getcwd()) != 'akebi':
        if not os.path.exists('akebi'):
            os.mkdir('akebi')
        os.chdir('akebi')

    if not os.path.exists('backup'):
        os.mkdir('backup')
    
    update_checks()

def update_checks():
    if not os.path.exists('update.json'):
        with open('update.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi()}))
            f.close()
    else:
        with open('update.json', 'r') as f:
            update_json = json.loads(f.read())

            if 'akebi' not in update_json:
                update_json['akebi'] = get_last_version()
                with open('update.json', 'w') as f:
                    json.dump(update_json, f)
                    f.close()

            if 'kebi' not in update_json:
                update_json['kebi'] = get_last_version_kebi()
                with open('update.json', 'w') as f:
                    json.dump(update_json, f)
                    f.close()
    create_ini()

def create_ini():
    with open('cfg.ini', 'w') as f:
        f.write('[Inject]\n')
        f.write('GenshinPath = ' + find_genshin() + '\GenshinImpact.exe')
        return True

def find_genshin():
    for root, dirs, files in os.walk(drive):
        if 'GenshinImpact.exe' in files: return root

def get_last_version():
    latest_version = subprocess.check_output(['curl', '-s', 'https://api.github.com/repos/Taiga74164/Akebi-GC/releases/latest']).decode('utf-8')
    latest_version = json.loads(latest_version)
    for asset in latest_version['assets']:
        if 'global' in asset['name']:
            return asset['browser_download_url']

def get_last_version_kebi():
    latest_version = subprocess.check_output(['curl', '-s', 'https://api.github.com/repos/menleev/kebi-loader/releases/latest']).decode('utf-8')
    latest_version = json.loads(latest_version)
    for asset in latest_version['assets']:
        if 'global' in asset['name']:
            return asset['browser_download_url']

def update_all():
    ch_a = check_version_akebi()
    if ch_a == 'akebi':
        update_akebi()
        os.system('cls')
    
    ch_k = check_version_kebi()
    if ch_k == 'kebi':
        update_kebi()
        os.system('cls')
    return True

def check_version_akebi():
    with open('update.json', 'r') as f:
        update_json = json.loads(f.read())
        if update_json['akebi'] != get_last_version():
            return 'akebi'

def check_version_kebi():       
    with open('update.json', 'r') as f:
        update_json = json.loads(f.read())
        if update_json['kebi'] != get_last_version_kebi():
            return 'kebi'

def update_kebi():
    latest_version = get_last_version_kebi()
    subprocess.call(['curl', '-L', latest_version, '-o', 'Kebi_Loader_new.exe'])
    with open('update.json', 'r') as f:
        data = json.loads(f.read())
    with open('update.json', 'w') as f:
        data['kebi'] = get_last_version_kebi()
        json.dump(data, f)
        f.close()
    os.system('cls')
    return True

def update_akebi():
    latest_version = get_last_version()
    subprocess.call(['curl', '-L', latest_version, '-o', 'akebi.zip'])
    with ZipFile('akebi.zip', 'r') as zipObj:
        zipObj.extractall()
    os.remove('akebi.zip')
    with open('update.json', 'r') as f:
        data = json.loads(f.read())
    with open('update.json', 'w') as f:
        data['akebi'] = get_last_version()
        json.dump(data, f)
        f.close()
    os.system('cls')
    return True

if __name__ == '__main__':
    menu()

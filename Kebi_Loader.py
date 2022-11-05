import json
import os
import subprocess
import time
import psutil
from zipfile import ZipFile

drive = psutil.disk_partitions()[0].device

def start():
    menu()

def menu():
    
    os.system('cls')
    print('ЧТОБЫ ЗАПУСТИТЬ ЧИТ НАЖМИТЕ ENTER НИЧЕГО НЕ ВВОДЯ\n')
    
    print('0.' '\033[31m ' 'Создает папку с конфигами и скаченной версией Akebi-GC''\033[0m')
    print('1. Обновить' '\033[35m ' 'Akebi-GC''\033[0m')
    print('2. Обновить ' '\033[36m' 'Kebi-Loader''\033[0m')
    print('3. Обновить ' '\033[31m' 'Оба файла ''\033[0m')
    print('\033[32m''Впишите цифру от пункта:''\033[0m')
    choice = input()
    if choice == '0':
        winv()
        menu()

    if choice == '1':
        update_akebi()
        menu()

    elif choice == '2':
        update_kebi()
        menu()

    elif choice == '3':
        update_all()
        menu()

    #если нажат enter
    elif choice == '':
        injector_start()
        menu()

#функция для проверки наличия папки akebi и backup
def winv():
    if os.path.basename(os.getcwd()) != 'akebi':
        if not os.path.exists('akebi'):
            os.mkdir('akebi')
        os.chdir('akebi')

    if not os.path.exists('backup'):
        os.mkdir('backup')
    
    update_checks()

#функция для проверки новой версии и обновления
def update_checks():
    if not os.path.exists('update_cfg_kebi.json'):
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()
    elif os.path.getsize('update_cfg_kebi.json') == 0:
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()
    else:
        with open('update_cfg_kebi.json', 'r') as f:
            update_json = json.loads(f.read())
            f.close()

            if 'akebi' not in update_json:
                update_json['akebi'] = get_last_version()
                with open('update_cfg_kebi.json', 'w') as f:
                    json.dump(update_json, f, indent=4)
                    f.close()

            if 'kebi' not in update_json:
                update_json['kebi'] = get_last_version_kebi()
                with open('update_cfg_kebi.json', 'w') as f:
                    json.dump(update_json, f, indent=4)
                    f.close()

    create_ini()

#функция для создания ini файла с указанием пути к игре для акеби
def create_ini():
    with open('cfg.ini', 'w') as f:
        f.write('[Inject]\n')
        f.write('GenshinPath = ' + find_genshin() + '\GenshinImpact.exe')
        
        update_akebi()
        

#функция для поиска пути к игре
def find_genshin():
    for root, dirs, files in os.walk(drive):
        if 'GenshinImpact.exe' in files: return root

#функция для получения последней версии akebi
def get_last_version():
    latest_version = subprocess.check_output(['curl', '-s', 'https://api.github.com/repos/Taiga74164/Akebi-GC/releases/latest']).decode('utf-8')
    latest_version = json.loads(latest_version)
    for asset in latest_version['assets']:
        if 'global' in asset['name']:
            return asset['browser_download_url']

#функция для получения последней версии kebi
def get_last_version_kebi():
    latest_version = subprocess.check_output(['curl', '-s', 'https://api.github.com/repos/menleev/kebi-loader/releases/latest']).decode('utf-8')
    latest_version = json.loads(latest_version)
    for asset in latest_version['assets']:
        if 'global' in asset['name']:
            return asset['browser_download_url']

#функция для обновления akebi и kebi
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

#функция для проверки версии akebi
def check_version_akebi():
    with open('update_cfg_kebi.json', 'r') as f:
        update_json = json.loads(f.read())
        if update_json['akebi'] != get_last_version():
            return 'akebi'

#функция для проверки версии kebi
def check_version_kebi():       
    with open('update_cfg_kebi.json', 'r') as f:
        update_json = json.loads(f.read())
        if update_json['kebi'] != get_last_version_kebi():
            return 'kebi'

#функция для обновления akebi
def update_kebi():
    latest_version = get_last_version_kebi()
    subprocess.call(['curl', '-L', latest_version, '-o', 'Kebi_Loader_new.exe'])

    with open('update_cfg_kebi.json', 'r') as f:
        data = json.loads(f.read())
    with open('update_cfg_kebi.json', 'w') as f:
        data['kebi'] = get_last_version_kebi()
        json.dump(data, f, indent=4)
        f.close()

    os.system('cls')
    return True

#функция для обновления kebi
def update_akebi():
    latest_version = get_last_version()

    if os.path.exists('injector.exe') and os.path.exists('CLibrary.dll'):
        os.remove('injector.exe')
        os.remove('CLibrary.dll')

    subprocess.call(['curl', '-L', latest_version, '-o', 'akebi.zip'])

    with ZipFile('akebi.zip', 'r') as zipObj:
        zipObj.extractall()
    os.remove('akebi.zip')

    with open('update_cfg_kebi.json', 'r') as f:
        data = json.loads(f.read())
    with open('update_cfg_kebi.json', 'w') as f:
        data['akebi'] = get_last_version()
        json.dump(data, f, indent=4)
        f.close()

    os.system('cls')
    return True

#функция для поиск инжектора
def inject_find(injector):
    for root, dirs, files in os.walk(drive):
        if 'Recycle.Bin' not in root:
            if 'update_cfg_kebi.json' in files: 
                for inject, dirs, files in os.walk(root):
                    if 'injector.exe' in files:
                        injector = inject + '\injector.exe'
                        return injector
                    else: 
                        up = update_akebi()
                        if up == True:
                            injector = inject + '\injector.exe'
                            print(injector)
                            return injector

#функция для записи в cfg пути к инжектору
def inject_starting(injector):
    try:
        with open('update_cfg_kebi.json', 'r') as f:
            data = json.loads(f.read())

        injector = inject_find(injector)
        with open('update_cfg_kebi.json', 'w') as f:
            data['injector'] = injector
            json.dump(data, f, indent=4)
            f.close()
    except:
        os.system('cls')
        return True

#функция для запуска игры
def injector_start():
    injector = None
    inject_starting(injector)
    try:
        with open('update_cfg_kebi.json', 'r') as f:
            data = json.loads(f.read())
            f.close()

        if not os.path.exists('cfg.ini'):
            create_ini()
        inject = [data['injector'], 'cfg.ini']
        subprocess.Popen(inject, creationflags=subprocess.CREATE_NEW_CONSOLE)
        os.system('cls')
        return True

    except UnboundLocalError:
        os.system('cls')
        return True

    except FileNotFoundError:
        os.system('cls')
        return True

if __name__ == '__main__':
    start()

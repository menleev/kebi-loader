import json
import os
import shutil
import subprocess
import time
import zipfile
import psutil
from zipfile import ZipFile

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
        if winv() == True:
            print('Папка с конфигами и скаченной версией Akebi-GC создана')
            time.sleep(3)
            menu()
        else:
            print('Ошибка')
            time.sleep(3)
            menu()
        
    if choice == '1':
        if update_akebi() == True:
            print('Akebi-GC обновлен')
            time.sleep(3)
            menu()
        else:
            print('Ошибка')
            time.sleep(3)
            menu()

    elif choice == '2':
        if update_kebi() == True:
            print('Kebi-Loader обновлен')
            time.sleep(3)
            menu()
        else:
            print('Ошибка')
            time.sleep(3)
            menu()

    elif choice == '3':
        if update_kebi() == True:
            print('Всё обновлено')
            time.sleep(3)
            menu()
        else:
            print('Ошибка')
            time.sleep(3)
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
    
    create_cfg()
    create_ini()
    update_akebi()
    update_kebi()
    return True

#функция для проверки новой версии и обновления
def create_cfg():
    if not os.path.exists('update_cfg_kebi.json'):
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()

    elif os.path.getsize('update_cfg_kebi.json') == 0:
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()
    
    return True

#функция для создания ini файла с указанием пути к игре для акеби
def create_ini():
    with open('cfg.ini', 'w') as f:
        f.write('[Inject]\n')
        f.write('GenshinPath = ' + find_genshin() + '\GenshinImpact.exe')
        
    return True
        
#функция для поиска пути к игре
def find_genshin():
    for disk in psutil.disk_partitions():
        for root, dirs, files in os.walk(disk.mountpoint):
            if 'GenshinImpact.exe' in files:
                return root

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
    update_akebi()
    update_kebi()
    os.system('cls')
    return True

#функция для обновления akebi
def update_kebi():
    try:
        latest_version = get_last_version_kebi()
        if get_data('akebi') == None:
            subprocess.call(['curl', '-L', latest_version, '-o', 'Kebi_Loader_new.exe'])
            os.system('cls')
            return False
        else:
            subprocess.call(['curl', '-L', latest_version, '-o', get_data('akebi') + '\\Kebi_Loader_new.exe'])
            os.system('cls')
            return True
    except FileNotFoundError:
       return False
    except TypeError:
        return False
    except PermissionError:
        return False

#функция для обновления kebi
def update_akebi():
    try:
        latest_version = get_last_version()
        if get_data('akebi') == None:
            subprocess.call(['curl', '-L', latest_version, '-o', 'akebi.zip'])
            with zipfile.ZipFile('akebi.zip', 'r') as zip_ref:
                zip_ref.extractall()
            os.remove('akebi.zip')
            os.system('cls')
            return False

        else:
            subprocess.call(['curl', '-L', latest_version, '-o', get_data('akebi') + '\\akebi.zip'])
            with zipfile.ZipFile(get_data('akebi')) as zip_ref:
                zip_ref.extractall()
            os.remove(get_data('akebi'))
            return True
    except FileNotFoundError:
       return False
    except TypeError:
        return False
    except PermissionError:
        return False

#поиск
def get_data(data):
    try:
        for korneplod in os.listdir(os.getcwd()):
            if data in korneplod:
                injector_path = os.path.abspath(korneplod)
                return injector_path
        else:
            for disk in psutil.disk_partitions():
                for root, dirs, files in os.walk(disk.mountpoint):
                    if 'Recycle.Bin' not in root:
                        if 'update_cfg_kebi.json' in files:
                            return root
    except FileNotFoundError:
       return False
    except TypeError:
        return False
    except PermissionError:
        return False

#функция для запуска игры
def injector_start():
    try:
        if get_data('injector.exe') == None:
            print('Не найден cfg.ini и update_cfg_kebi.json')
            return False
        else:
            subprocess.Popen(get_data('injector.exe') + '\\injector.exe', creationflags=subprocess.CREATE_NEW_CONSOLE)
            os.system('cls')
            return True
    except FileNotFoundError:
       return False
    except TypeError:
        return False
    except PermissionError:
        return False
if __name__ == '__main__':
    menu()

import json
import os
import shutil
import subprocess
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
        subprocess.call(['curl', '-L', latest_version, '-o', 'Kebi_Loader_new.exe'])
        if folder_find() == None:
            os.system('cls')
            return False

        shutil.move('Kebi_Loader_new.exe', folder_find() + '\\Kebi_Loader.exe')

        os.system('cls')
        return True
    except FileNotFoundError:
        return False

#функция для обновления kebi
def update_akebi():
    try:
        latest_version = get_last_version()
        if folder_find() == None:
            subprocess.call(['curl', '-L', latest_version, '-o', 'akebi.zip'])
            #распаковка архива
            with zipfile.ZipFile('akebi.zip', 'r') as zip_ref:
                zip_ref.extractall()
            os.remove('akebi.zip')
            return False
        else:
            subprocess.call(['curl', '-L', latest_version, '-o', folder_find() + '\\akebi.zip'])
            with ZipFile(folder_find() + '\\akebi.zip', 'r') as zipObj:
                zipObj.extractall(folder_find())
            os.remove(folder_find()+'\\akebi.zip')
            os.system('cls')
            return True
    except FileNotFoundError:
        os.system('cls')
        return False

#функция для поиска пути к папке с akebi
def folder_find():
    try:
        for disk in psutil.disk_partitions():
            for root, dirs, files in os.walk(disk.mountpoint):
                if 'Recycle.Bin' not in root:
                    if 'update_cfg_kebi.json' in files:
                        fol_f = root
                        return fol_f
    except FileNotFoundError:
       return False
    except TypeError:
        return False

#функция для поиска пути к update_cfg_kebi.json
def cfg_find():
    try:
        for disk in psutil.disk_partitions():
            for root, dirs, files in os.walk(disk.mountpoint):
                if 'Recycle.Bin' not in root:
                    if 'update_cfg_kebi.json' in files:
                        cfg_k = root
                        return cfg_k + '\\update_cfg_kebi.json'
    except FileNotFoundError:
       return False
    except TypeError:
        return False

#поиск injector
def inj_find():
    try:
        for disk in psutil.disk_partitions():
            for root, dirs, files in os.walk(disk.mountpoint):
                if 'Recycle.Bin' not in root:
                    if 'update_cfg_kebi.json' in files:
                        cfg_f = root
                        return cfg_f + '\injector.exe'
    except FileNotFoundError:
       return False

#поиск cfg.ini
def ini_find():
    try:
        for disk in psutil.disk_partitions():
            for root, dirs, files in os.walk(disk.mountpoint):
                if 'Recycle.Bin' not in root:
                    if 'update_cfg_kebi.json' in files:
                        for inject, dirs, files in os.walk(root):
                            if 'cfg.ini' in files:
                                cfg_i = inject + '\cfg.ini'
                                return cfg_i
    except FileNotFoundError:
       return False

#функция для запуска игры
def injector_start():
    try:
        inj_f = inj_find()
        if inj_f == None:
            print('Инжектор не найден')
            return False

        ini_f = ini_find()
        if ini_f == None:
            print('cfg.ini не найден')
            return False
        subprocess.Popen([inj_f, ini_f], creationflags=subprocess.CREATE_NEW_CONSOLE)
        os.system('cls')
        return True
    except TypeError:
        os.system('cls')
        return False
    except UnboundLocalError:
       os.system('cls')
       return False
    except PermissionError:
        os.system('cls')
        return False
    except FileNotFoundError:
        os.system('cls')
        return False


if __name__ == '__main__':
    menu()

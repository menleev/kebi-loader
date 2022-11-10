import json
import multiprocessing
import threading
import win32api
import os
import subprocess
import sys
import time
import zipfile
import psutil

cfg_winde = None

def winv():
    create_cfg()
    create_ini()
    update_kebi()
    update_akebi()
    download_teleport()
    print('[o] Всё готово, приятной игры!\n')
    sys.exit()

#функция для проверки новой версии и обновления
def create_cfg():
    print('[o] Проверка наличия файла конфигурации\n')
    if not os.path.exists('update_cfg_kebi.json'):
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()

    elif os.path.getsize('update_cfg_kebi.json') == 0:
        with open('update_cfg_kebi.json', 'w') as f:
            f.write(json.dumps({'akebi': get_last_version(), 'kebi': get_last_version_kebi(), 'injector': 'C:\\'}, indent=4))
            f.close()
    global cfg_winde
    cfg_winde = os.path.abspath(os.path.join('update_cfg_kebi.json', os.pardir))
    print('[o] Файл конфигурации найден\n')
    return True

#функция для создания ini файла с указанием пути к игре для акеби
def create_ini():
    print('[o] Проверка наличия файла cfg.ini\n')
    start('GenshinImpact.exe')
    if not os.path.exists('cfg.ini'):
        #создание ini файла
        with open('cfg.ini', 'w') as f:
            f.write('[Inject]\n')
            f.write('GenshinPath = ' + game_patch + '\GenshinImpact.exe')
            f.close()
        print('[o] Файл cfg.ini найден\n')
        return True
    else:
        print('[o] Файл cfg.ini найден\n')
        return True

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

#функция для обновления akebi
def update_kebi():
    try:
        kebi_latest_version = get_last_version_kebi()
        if cfg_winde == None:
            start('akebi')
            if game_patch == None:
                subprocess.call(['curl', '-L', kebi_latest_version, '-o', 'Kebi_Loader.exe'])
                os.system('cls')
                return False
        else:
            print('[o] Проверка наличия актуальной версии kebi\n')
            with open(cfg_winde + '\\update_cfg_kebi.json', 'r') as f:
                data = json.load(f)
                f.close()
            print('[o] Проверка наличия актуальной версии kebi завершена\n')
            kebi_version = data['kebi']
            if kebi_version != kebi_latest_version:
                print('[o] Обновление kebi найдено приступаю к обновлению\n')
                if os.path.exists('Kebi_Loader.exe'):
                    i = 1
                    while os.path.exists('Kebi_Loader' + str(i) + '.exe'):
                        i += 1
                    subprocess.call(['curl', '-L', kebi_latest_version, '-o', 'Kebi_Loader' + str(i) + '.exe'])
                    data['kebi'] = kebi_latest_version
                    with open(cfg_winde + '\\update_cfg_kebi.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        f.close()
                        print('[o] Обновление kebi завершено\n')
                        return True
                else:
                    subprocess.call(['curl', '-L', kebi_latest_version, '-o', cfg_winde + '\\Kebi_Loader.exe'])
                    data['kebi'] = kebi_latest_version
                    with open(cfg_winde + '\\update_cfg_kebi.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        f.close()
                        print('[o] Обновление kebi завершено\n')
                        return True
            else:
                print('[o] Обновление kebi не найдено\n')
                return False
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
        if cfg_winde == None:
            start('akebi')
            if game_patch == None:
                subprocess.call(['curl', '-L', latest_version, '-o', 'akebi.zip'])
                with zipfile.ZipFile('akebi.zip', 'r') as zip_ref:
                    zip_ref.extractall()
                os.remove('akebi.zip')
                os.system('cls')
                return False
        else:
            print('[o] Проверка наличия файлов akebi\n')
            if not os.path.exists(cfg_winde + '\\CLibrary.dll') or not os.path.exists(cfg_winde + '\\injector.exe'):
                print('[o] Файлы akebi не найдены приступаю к загрузке\n')
                subprocess.call(['curl', '-L', latest_version, '-o', cfg_winde + '\\akebi.zip'])
                with zipfile.ZipFile(cfg_winde + '\\akebi.zip', 'r') as zip_ref:
                    zip_ref.extractall(cfg_winde)
                os.remove(cfg_winde + '\\akebi.zip')
                print('[o] Файлы akebi загружены\n')
                return True
            else:
                print('[o] Файлы akebi найдены\n')
                with open(cfg_winde + '\\update_cfg_kebi.json', 'r') as f:
                    data = json.load(f)
                    f.close()
                print('[o] Проверка наличия актуальной версии akebi\n')
                akebi_version = data['akebi']
                if akebi_version != latest_version:
                    print('[o] Обновление akebi найдено приступаю к обновлению\n')
                    subprocess.call(['curl', '-L', latest_version, '-o', cfg_winde + '\\akebi.zip'])
                    os.remove(cfg_winde + '\\CLibrary.dll') and os.remove(cfg_winde + '\\injector.exe')
                    with zipfile.ZipFile(cfg_winde + '\\akebi.zip', 'r') as zip_ref:
                        zip_ref.extractall(cfg_winde)
                    os.remove(cfg_winde + '\\akebi.zip')
                    data['akebi'] = latest_version
                    with open(cfg_winde + '\\update_cfg_kebi.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        f.close()
                        print('[o] Обновление akebi завершено\n')
                        return True
                else:
                    print('[o] Обновление akebi не найдено\n')
                    return False
    except FileNotFoundError:
       return False
    except TypeError:
        return False
    except PermissionError:
        return False

def download_teleport():
    subprocess.call(['curl', '-L', 'https://github.com/menleev/kebi-loader/raw/main/Good%20Teleport.zip', '-o', cfg_winde + '\\GoodTeleport.zip'])
    with zipfile.ZipFile(cfg_winde + '\\GoodTeleport.zip', 'r') as zip_ref:
        zip_ref.extractall(cfg_winde)
    os.remove(cfg_winde + '\\GoodTeleport.zip')
    return True

#функция которая создает потоки для вызова функций поиска
def start(game):
    disked = psutil.disk_partitions()
    th = []
    for disk in disked:
        t = threading.Thread(target=game_data, args=(disk, game))
        t.start()
        th.append(t)
    for t in th:
        t.join()
    return True

game_patch = None

def game_data(disk, game):
    start_time = time.time()
    print('[o] Поиск игры на диске ' + disk.device)
    for root, dirs, files in os.walk(disk.mountpoint):
        if game in files:
            global game_patch
            game_patch = root
            return True

if __name__ == '__main__':
    winv()

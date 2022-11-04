import os
import sys
import json
import subprocess
import win32api, win32con, win32gui
import psutil
from zipfile import ZipFile

def find_genshin():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if 'GenshinImpact.exe' in files:
                return root

def get_last_version():
    latest_version = subprocess.check_output(['curl', '-s', 'https://api.github.com/repos/Taiga74164/Akebi-GC/releases/latest']).decode('utf-8')
    latest_version = json.loads(latest_version)
    for asset in latest_version['assets']:
        if 'global' in asset['name']:
            return asset['browser_download_url']

def create_ini():
    with open('cfg.ini', 'w') as f:
        f.write('[Inject]\n')
        f.write('GenshinPath = ' + find_genshin() + '\GenshinImpact.exe' '\n')

def main():
    if os.path.basename(os.getcwd()) != 'akebi':
        if not os.path.exists('akebi'):
            os.mkdir('akebi')
        os.chdir('akebi')

    if not os.path.exists('backup'):
        os.mkdir('backup')

    if not os.path.exists('akebi_version.txt') or open('akebi_version.txt').read() != get_last_version():
        for file in os.listdir():
            if file != 'backup' and file != 'akebi_version.txt':
                if os.path.exists('backup\\' + file):
                    i = 1
                    while os.path.exists('backup\\' + str(i) + file):
                        i += 1
                    os.rename(file, 'backup\\' + str(i) + file)
                else:
                    os.rename(file, 'backup\\' + file)
        subprocess.run(['curl', '-L', get_last_version(), '-o', 'akebi.zip'])

        with ZipFile('akebi.zip', 'r') as zipObj:
            zipObj.extractall()
        os.remove('akebi.zip')

        with open('akebi_version.txt', 'w') as f:
            f.write(get_last_version())
            
    create_ini()

if __name__ == '__main__':
    main()

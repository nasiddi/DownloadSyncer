import pysftp
from os import listdir, path, remove
from sys import argv, exit
import json
import time
import _thread
from datetime import datetime
import platform

if platform.system() == 'Windows':
    DOWNLOAD_DIR = 'C:\\Users\\Nadina\\Downloads'
else:
    DOWNLOAD_DIR = '/Users/nadina/Downloads'
REMOTE_PATH = 'Temp/watch'
LOG = 'dsyncerlog.json'


if not path.exists(DOWNLOAD_DIR):
    print('Download Path is wrong')
    exit(0)


def main(name):
    if not name:
        print('Enter Client Name')
        exit(0)
    name = name[0]
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    while True:
        if a_list:
            a_list = []
            srv = connect()
            dt = datetime.now()
            if srv:
                print(dt.strftime("%Y-%m-%d %H:%M"), 'connected')
                srv.close()
            else:
                print(dt.strftime("%Y-%m-%d %H:%M"), 'not connected')
            _thread.start_new_thread(input_thread, (a_list,))
        files = listdir(DOWNLOAD_DIR)
        nzb_files = [path.join(DOWNLOAD_DIR, f) for f in files if f.endswith('.nzb') or f.startswith('dognzb')]
        if nzb_files:
            srv = connect()
            if not srv:
                continue
            srv.chdir(REMOTE_PATH)
            try:
                srv.get(LOG)
            except FileNotFoundError:
                pass
            j_data = load_json(LOG)
            if name not in j_data:
                j_data[name] = {'files': [], 'opened': True, 'key': name}

            for f in nzb_files:
                srv.put(f)
                print(f)
                remove(f)
                j_data[name]['files'].append(path.basename(f))

            while len(j_data[name]) > 20:
                j_data[name].pop(0)
            save_json(j_data, LOG)
            srv.put(LOG)
            srv.close()
            remove(LOG)

        time.sleep(3)


def connect():
    try:
        return pysftp.Connection(host="skyship.space", username="nadina", password="Sherlock69")
    except:
        return None


def input_thread(a_list):
    input()
    a_list.append(True)


def save_json(data_json, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_json, indent=4, sort_keys=True, ))


def load_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as json_data:
            j_data = json.load(json_data)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}
    return j_data


if __name__ == '__main__':
    main(argv[1:])

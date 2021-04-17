import os
from os import path, mkdir, makedirs, access
from datetime import datetime
import subprocess
import re
import gzip
from notification import SendMail
from config import config, APP_DIR

BACKUP_DIR = path.join(APP_DIR, 'backup')

if not path.exists(BACKUP_DIR):
    mkdir(BACKUP_DIR)
elif not access(BACKUP_DIR, os.W_OK):
    print('Директория %s не доступна для записи' % BACKUP_DIR)
    exit(1)

cmd = "mysqldump -h {host} -P {port} -u{user} -p{password} {dbname}".format(**config['database'])
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()

errors = err.decode('utf-8').split("\n")
regexp = r'error:\s+(\d+):\s+(.+)'
errors = [e for e in errors if re.search(regexp, e) is not None]

if len(errors) > 0:
    print(errors[0])
    exit(2)

BACKUP_SUB_DIR = path.join(BACKUP_DIR, datetime.now().strftime('%Y/%m/%d'))

if not path.exists(BACKUP_SUB_DIR):
    makedirs(BACKUP_SUB_DIR, mode=0o755, exist_ok=True)

backup_filename = '{0}-{1}.sql.gz'.format(config['database']['dbname'], datetime.now().strftime('%Y%m%d%H%M%S'))
backup_file_path = path.join(BACKUP_SUB_DIR, backup_filename)

with gzip.open(backup_file_path, 'wb') as fp:
    fp.write(out)


sender = SendMail(**config['smtp'])
sender.send(config['receiver'], 'Резервное копирование базы данных',
            'Резервное копирование базы данных {dbname} выполнена'.format(**config['database']))


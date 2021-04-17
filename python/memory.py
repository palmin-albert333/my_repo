from subprocess import Popen, PIPE
from notification import SendMail
from config import config
import re

"""
Мониторинг файла подкачки.
"""

proc = Popen(['free', '-m'], stdout=PIPE)
[header, mem, swap] = [s.decode('utf-8').strip() for s in proc.stdout.readlines()]

int_matcher = re.compile(r'\d+')

header = re.split(r'\s+', header)
mem = dict(zip(header, map(int, int_matcher.findall(mem))))
swap = dict(zip(header[:3], map(int, int_matcher.findall(swap))))

mem['used_percent'] = round(mem['used'] / mem['total'] * 100, 2)
swap['used_percent'] = round(swap['used'] / swap['total'] * 100, 2)

if swap['used_percent'] > 0:
    sender = SendMail(**config['smtp'])
    sender.send(config['receiver'], 'Memory limit', "\n".join([
        'Memory limit.',
        'Memory limit {used_percent} %'.format(**mem)
    ]))

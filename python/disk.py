from subprocess import Popen, PIPE
from notification import SendMail
from config import config
import re


def disk_stat(disk):
    proc = Popen('df %s' % disk, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = (s.decode('utf-8') for s in proc.communicate())
    res = map(float, re.split(r'\s+', out.split("\n")[1])[1:4])
    res = dict(zip(('total', 'used', 'avail'), res))

    try:
        res['use_percent'] = round((res['used'] / res['total']) * 100, 1)
    except ZeroDivisionError:
        res['use_percent'] = 0

    return res


stat = disk_stat('/dev/sda1')

if stat['use_percent'] > 90:
    sender = SendMail(**config['smtp'])
    sender.send(config['receiver'], 'Диск переполнен', "\n".join([
        'Диск переполнен.',
        'Занято {use_percent} %'.format(**stat)
    ]))

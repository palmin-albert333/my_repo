import os
import re
from datetime import datetime
from config import config, APP_DIR
from notification import SendMail

"""
Проверка попыток входа по SSH
"""

DATETIME_ISO_FORMAT = '%Y-%m-%d %H:%M:%S'
AUTH_LOG_FILE = '/var/log/auth.log'


def failured_auths(start_dt=None):
    log_size = os.path.getsize(AUTH_LOG_FILE)

    regexp_ssh = r'^([A-Z][a-z]+ \d{2} \d{2}:\d{2}:\d{2}) [-\w]+ sshd\[\d+\]: '
    regexp = regexp_ssh + r'PAM 2 more authentication failures; (.+)$'
    regexp_invalid_user = regexp_ssh + r'Invalid user ([^\s]+) from ([^\s]+) port (\d+)'
    current_dt = datetime.now().replace(microsecond=0)

    last_rows = []
    failures = {}

    with open(AUTH_LOG_FILE, 'r') as fp:
        while fp.tell() < log_size:
            last_rows.insert(0, fp.readline().rstrip())
            match = re.search(regexp, last_rows[0])
            if match is not None:
                dt, msg = match.groups()
                dt = datetime.strptime('%s %s' % (current_dt.year, dt), '%Y %b %d %H:%M:%S')

                if start_dt is None or start_dt > dt:
                    continue

                info = dict(re.findall(r'(\w+)=([^=\s]+)', msg))
                info['invalid'] = False

                if 'user' not in info:
                    for row in last_rows:
                        invalid_user_match = re.search(regexp_invalid_user, row)
                        if invalid_user_match is not None:
                            info['user'] = invalid_user_match.group(2)
                            info['invalid'] = True
                            break

                if info['rhost'] not in failures:
                    failures[info['rhost']] = dict(rhost=info['rhost'], auths={})

                if info['user'] not in failures[info['rhost']]['auths']:
                    failures[info['rhost']]['auths'][info['user']] = dict(
                        user=info['user'], last_dt=None, count=0
                    )

                auth = failures[info['rhost']]['auths'][info['user']]
                auth['last_dt'] = dt.strftime(DATETIME_ISO_FORMAT)
                auth['count'] += 1

    failures = list(failures.values())

    for failure in failures:
        failure['auths'] = list(failure['auths'].values())

    return failures


def main():
    log_file = os.path.join(APP_DIR, 'ssh_auth_failure.log')
    last_scan_dt = None

    if os.path.exists(log_file):
        with open(log_file, 'r') as fp:
            last_scan_dt = datetime.strptime(fp.readline().rstrip(), DATETIME_ISO_FORMAT)

    with open(log_file, 'w') as fp:
        fp.write(datetime.now().replace(microsecond=0).strftime(DATETIME_ISO_FORMAT))

    _failured_auths = failured_auths(last_scan_dt)

    if len(_failured_auths) > 0:
        message_rows = ['Попытки входа по SSH', '']

        for failured_auth in _failured_auths:
            message_rows.append('Хост: {rhost}'.format(**failured_auth))

            for auth in failured_auth['auths']:
                message_rows.append(
                    '\tПользователь: {user}\n'
                    '\tКоличество попыток: {count}\n'
                    '\tДата/время последней попытки: {last_dt}\n'
                    ''.format(**auth)
                )

        sender = SendMail(**config['smtp'])
        sender.send(config['receiver'], 'Попытки входа по SSH', '\n'.join(message_rows))


if __name__ == '__main__':
    main()




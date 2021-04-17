import urllib.request
import urllib.error
from notification import SendMail
from config import config


def check_website_availability(url):
    try:
        return urllib.request.urlopen(url).getcode() == 200
    except urllib.error.URLError as e:
        return False


domain = 'eios.imsit.ru'

if not check_website_availability("http://%s" % domain):
    sender = SendMail(**config['smtp'])
    sender.send(config['receiver'], 'Сайт не доступен', 'Сайт %s не доступен' % domain)
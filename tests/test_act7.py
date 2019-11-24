from bs4 import BeautifulSoup
import requests


# Activity 7 test
def test_command_injection():
    login = requests.get("http://localhost:5000/adduser", {"username": "uniquename", "password": "password", "displayname": "uniquename", "command": "whoami"}).text
    soup = BeautifulSoup(login, "html.parser")
    text=soup.find_all(text=True)
    print(text)
    assert "root" in text

if __name__ == '__main__':
    test_command_injection()
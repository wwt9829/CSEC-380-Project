from bs4 import BeautifulSoup
import requests
from os import urandom


# Activity 7 test
def test_command_injection():
    # Create unique name
    name = urandom(8).hex()
    login = requests.get("http://localhost:5000/adduser", {"username": name, "password": "password", "displayname": name, "command": "whoami"}).text
    soup = BeautifulSoup(login, "html.parser")
    text=soup.find_all(text=True)
    print(text)
    assert "root\n" in text

if __name__ == '__main__':
    test_command_injection()
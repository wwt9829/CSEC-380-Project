from bs4 import BeautifulSoup
import requests


# Activity 3 tests
def test_successful_login():
    login = requests.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text
    soup = BeautifulSoup(login, "html.parser")
    text=soup.find_all(text=True)
    print(text)
    assert "Test Test's ChaimTube" in text


def test_invalid_password():
    invalid_pass = requests.post("http://localhost:5000/login", {"username": "test@user.com", "password": "wrongpassword"}).text
    assert "That username and password combination does not exist." in invalid_pass


def test_invalid_username():
    invalid_name = requests.post("http://localhost:5000/login", {"username": "fakeuser", "password": "changeme"}).text
    assert "That username and password combination does not exist." in invalid_name


if __name__ == '__main__':
    test_successful_login()
    test_invalid_password()
    test_invalid_username()
from bs4 import BeautifulSoup
import requests

def test_act6():
    session = requests.session()
    login = session.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text
    send_ssrf = session.post("http://localhost:5000/home", data={'submit': 'linkupload'}, files={'linkupload': 'http://www.google.com/'}).content
    soup = BeautifulSoup(send_ssrf, "html.parser")
    print(soup.prettify)    

if __name__ == "__main__":
    test_act6()

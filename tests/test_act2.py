from bs4 import BeautifulSoup
import requests


def get_page(url):
        r = requests.get(url)
        return r


def test_get_page():
        r = get_page("http://localhost:5000/").content
        soup = BeautifulSoup(r, "html.parser")
        text=soup.find_all(text=True)
        assert "ChaimTube" in text


if __name__ == '__main__':
        test_get_page()
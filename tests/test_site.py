from bs4 import BeautifulSoup
import requests


def get_page(url):
        r = requests.get(url)
        return r


def test_get_page():
        r = get_page("http://localhost/").content
        parsed_html = BeautifulSoup(r, "html.parser")
        body = parsed_html.body
        assert "Hello World" in str(body)


if __name__ == '__main__':
        test_get_page()
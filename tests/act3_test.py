import requests

# Activity 3 tests
def successful_login():
    login = requests.post("http://localhost:5000", {"username": "admin", "password": "changeme"}).text
    return "Successful login" in login

def invalid_password():
    invalid_pass = requests.post("http://localhost:5000", {"username": "admin", "password": "wrongpassword"}).text
    return "Incorrect password" in invalid_pass

def invalid_username():
    invalid_name = requests.post("http://localhost:5000", {"username": "fakeuser", "password": "changeme"}).text
    return "Incorrect username" in invalid_name

def main():
    assert successful_login()
    assert invalid_password()
    assert invalid_username()

if __name__ == '__main__':
    main()
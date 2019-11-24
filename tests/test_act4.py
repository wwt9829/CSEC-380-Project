import requests
import pytest

# Activity 4 test. Code signs in as a user, uploads a video, views the video, then deletes the video.
def test_act4():
    session = requests.session()
    login = session.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text

    with open('./tests/small.mp4', 'rb') as file:
        upload_file = session.post("http://localhost:5000/home", data={'submit': 'Upload'}, files={'file': file}).text
    assert "Test Test's ChaimTube" in upload_file   # Not sure what to assert here

    view_video = session.get("http://localhost:5000/video/small.mp4").status_code
    assert view_video == 200                        # Only thing I found usable was the status code

    # Video ID is only 1 the first time this test is ran. It will not work if videos have been added before running.
    # In order to work after that first initial run, the 1 must be changed to match the ID of the video to delete.
    delete_video = session.get("http://localhost:5000/delete/1").text
    assert "Test Test's ChaimTube" in delete_video  # Again, not sure what else to assert

if __name__ == '__main__':
    test_act4()

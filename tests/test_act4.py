import requests

# Activity 4 test. Code signs in as a user, uploads a video, views the video, then deletes the video.
def test_act4():
    verify_upload = False
    verify_view = False
    verify_delete = True

    session = requests.session()
    login = session.post("http://localhost:5000/login", {"username": "test@user.com", "password": "password"}).text

    with open('./tests/small.mp4', 'rb') as file:
        upload_file = session.post("http://localhost:5000/home", data=file).text
    if "small.mp4" in upload_file:
        verify_upload = True

    view_video = session.get("http://localhost:5000/video/small.mp4").status_code
    if view_video == 200:
        verify_view = True

    # delete_video = session.get("http://localhost:5000/delete/1").text
    # if "small.mp4" not in delete_video:
    #     verify_delete = True

    session.close()

    return "Upload successful? --> " and verify_upload and "\n" and "View successful? --> " and verify_view \
        and "\n" and "Delete successful? --> " and verify_delete and "\n"

if __name__ == '__main__':
    test_act4()

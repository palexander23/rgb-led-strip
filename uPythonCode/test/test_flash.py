import requests
from time import sleep


def check_response(res):
    print(res.request.body)
    assert res.status_code == 200


def test_flash():
    print("Sending..")
    res = requests.post(
        "http://192.168.0.107/",
        json={
            "mode": "flash",
            "colour_list": ["#ff0000", "#00ff00", "#0000ff"],
            "on_time_list": ["0.1", "0.1", "0.1"],
        },
    )
    check_response(res)

    sleep(1)

    print("Sending..")
    res = requests.post(
        "http://192.168.0.107/",
        json={
            "mode": "flash",
            "colour_list": ["#ff0000", "#550000", "#000000", "#550000"],
            "on_time_list": ["0.1", "0.1", "0.1", "0.1"],
        },
    )
    check_response(res)
    sleep(1)

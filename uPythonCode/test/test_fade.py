import requests
from time import sleep


def check_response(res):
    print(res.request.body)
    assert res.status_code == 200


def test_flash():
    print("Sending..")
    res = requests.post(
        "http://192.168.1.166/",
        json={
            "mode": "fade",
            "colour_list": ["#ff0000", "#00ff00", "#0000ff"],
            "on_time_list": ["0.5", "0.5", "0.5"],
            "fade_time_list": ["0.5", "0.5", "0.5"],
        },
    )
    check_response(res)

    sleep(3)

    print("Sending..")
    res = requests.post(
        "http://192.168.1.166/",
        json={
            "mode": "fade",
            "colour_list": ["#ff0000", "#110000"],
            "on_time_list": ["1", "0"],
            "fade_time_list": ["1", "1"],
        },
    )
    check_response(res)

    sleep(3)

    print("Sending..")
    res = requests.post(
        "http://192.168.1.166/",
        json={
            "mode": "fade",
            "colour_list": [
                "#ff0000",
                "#000000",
                "#00ff00",
                "#000000",
                "#0000ff",
                "#000000",
            ],
            "on_time_list": ["1", "0", "1", "0", "1", "0"],
            "fade_time_list": ["1", "1", "1", "1", "1", "1"],
        },
    )
    check_response(res)

    sleep(3)

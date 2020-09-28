import requests
from time import sleep


def check_response(res):
    print(res)
    assert res.status_code == 200


def test_basic_flash():
    print("Sending..")
    res = requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "blu": "ON", "red": "ON", "gre": "ON"},
    )
    check_response(res)
    sleep(0.5)

    res = requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "blu": "OFF", "red": "OFF", "gre": "OFF"},
    )
    sleep(0.5)
    check_response(res)

    print("Sent!")


def test_analog_brightness():
    print("Sending..")

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#6622ff"},
    )
    check_response(res)
    sleep(0.5)

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#66ff22"},
    )
    sleep(0.5)
    check_response(res)

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#6622ff"},
    )
    check_response(res)
    sleep(0.5)

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#66ff22"},
    )
    sleep(0.5)
    check_response(res)

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#6622ff"},
    )
    check_response(res)
    sleep(0.5)

    res = requests.post(
        "http://192.168.0.107/", json={"mode": "analog", "colour": "#66ff22"},
    )
    sleep(0.5)
    check_response(res)

    res = requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "blu": "OFF", "red": "OFF", "gre": "OFF"},
    )
    sleep(0.5)
    check_response(res)

    print("Sent!")

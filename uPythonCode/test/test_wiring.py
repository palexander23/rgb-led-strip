import requests, time


def test_wiring():
    print("Wiring Test")

    print("Red ON")
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "ON", "gre": "OFF", "blu": "OFF"},
    )
    time.sleep(1)
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "OFF", "gre": "OFF", "blu": "OFF"},
    )

    print("Green ON")
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "OFF", "gre": "ON", "blu": "OFF"},
    )
    time.sleep(1)
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "OFF", "gre": "OFF", "blu": "OFF"},
    )

    print("Blue ON")
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "OFF", "gre": "OFF", "blu": "ON"},
    )
    time.sleep(1)
    requests.post(
        "http://192.168.0.107/",
        json={"mode": "switch", "red": "OFF", "gre": "OFF", "blu": "OFF"},
    )

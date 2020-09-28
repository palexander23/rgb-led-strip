import requests


def test_single_request():
    res = requests.post(
        "http://192.168.0.107/", json={"key": "value", "key2": ["list1", "list2"]}
    )

    assert res.status_code == 400

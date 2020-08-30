import requests


def test_single_request():
    res = requests.post(
        "http://192.168.1.166/", json={"key": "value", "key2": ["list1", "list2"]}
    )

    assert res.status_code == 400


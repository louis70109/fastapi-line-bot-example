import os
import unittest
from _pytest.monkeypatch import MonkeyPatch
from mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_read_bot():
    import base64
    import hashlib
    import hmac

    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    body = '{"events":[],"destination":"U000000000000000000000003d9"}'
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    response = client.post(
        url="/webhooks/line",
        data=body,
        headers={
            "Content-Type": "multipart/form-data",
            'X-Line-Signature': signature.decode('UTF-8')
        })

    assert response.url == 'http://testserver/webhooks/line'
    assert response.status_code == 200
    assert response.json() == 'OK'

# class TestClient(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_read_main(self):
#         response = client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "Hello World!"})

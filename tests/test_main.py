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
    response = client.post("/webhooks/line", data=b'{"events":[],"destination":"U000000000000000000000003d9"}',
                           headers={"Content-Type": "multipart/form-data", 'X-Line-Signature': '123123'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'chatbot handle body error.'}

# class TestClient(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_read_main(self):
#         response = client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "Hello World!"})

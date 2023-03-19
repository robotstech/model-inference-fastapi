import json

from fastapi.testclient import TestClient

from model_inference_fastapi.main import app

client = TestClient(app)


def test_base_endpoint():
    response = client.get('/')
    assert response.status_code == 400


def test_ping_endpoint():
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.content == b'"pong"'


def test_predict_endpoint_with_get_method():
    response = client.get('/predict/')
    assert response.status_code == 405


def test_predict_endpoint_with_no_data():
    response = client.post('/predict/')
    assert response.status_code == 400


def test_predict_endpoint_with_bad_data():
    response = client.post('/predict/', json=[])
    assert response.status_code == 400


def test_predict_endpoint_with_valid_data():
    json_data = {"data": [{}]}
    bytes_data = bytes()
    files = {"uploaded_files": ("file_name", bytes_data, "multipart/form-data")}
    response = client.post('/predict/', data={"json_data": json.dumps(json_data)}, files=files)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data == [{"status": "Ready to Go!!!"}]

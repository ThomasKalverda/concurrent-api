import pytest

from app import app, get_data_store, reset_data_store


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def setup():
    reset_data_store()


def test_add_data(client):
    response = client.post("/data", json={"data": [1, 2, 3, 4]})
    assert response.status_code == 200
    assert response.json == {"message": "Data stored successfully"}
    assert get_data_store() == [1, 2, 3, 4]

    # Test adding more data replaces old data
    response = client.post("/data", json={"data": [5, 6, 7, 8]})
    assert response.status_code == 200
    assert response.json == {"message": "Data stored successfully"}
    assert get_data_store() == [5, 6, 7, 8]


def test_add_data_invalid(client):
    # Test no data
    response = client.post("/data", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input, provide a list of integers."}

    # Test empty list
    response = client.post("/data", json={"data": []})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input, provide a list of integers."}

    # Test not all integers
    response = client.post("/data", json={"data": [1, 2, 3, "4"]})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input, provide a list of integers."}

    # Test not a list
    response = client.post("/data", json={"data": 1})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input, provide a list of integers."}


def test_get_sorted_data(client):
    client.post("/data", json={"data": [3, 2, 1, 4]})
    response = client.get("/process/sort")
    assert response.status_code == 200
    assert response.json == {"sorted_data": [1, 2, 3, 4]}


def test_get_top_n(client):
    client.post("/data", json={"data": [3, 2, 1, 4]})
    response = client.get("/process/top-n?n=2")
    assert response.status_code == 200
    assert response.json == {"top_n": [4, 3]}


def test_get_top_n_invalid(client):
    client.post("/data", json={"data": [3, 2, 1, 4]})

    # Test n <= 0
    response = client.get("/process/top-n?n=0")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid value for n"}

    # Test n > len(data_store)
    response = client.get("/process/top-n?n=5")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid value for n"}

    # Test n not an integer
    response = client.get("/process/top-n?n=abc")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid value for n"}


def test_get_mean(client):
    client.post("/data", json={"data": [3, 2, 1, 4]})
    response = client.get("/process/mean")
    assert response.status_code == 200
    assert response.json == {"mean": 2.5}


def test_get_mean_empty(client):
    response = client.get("/process/mean")
    assert response.status_code == 200
    assert response.json == {"mean": 0}

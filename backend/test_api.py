from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_server_health():
    """Verify backend is alive"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_prediction_accuracy():
    """Verify model returns a valid number"""
    sample_car = {
        "cylinders": 4, "displacement": 120, "horsepower": 80,
        "weight": 2100, "acceleration": 16, "model_year": 78, "origin": 2
    }
    response = client.post("/predict", json=sample_car)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

def test_latency_performance():
    """Verify inference is faster than 100ms"""
    sample_car = {
        "cylinders": 8, "displacement": 350, "horsepower": 160,
        "weight": 4000, "acceleration": 12, "model_year": 70, "origin": 1
    }
    start = time.time()
    client.post("/predict", json=sample_car)
    latency = (time.time() - start) * 1000
    print(f"\nLatency: {latency:.2f}ms")
    assert latency < 100  # SDE requirement for high-speed APIs
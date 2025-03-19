from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Testing for root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI is working!"}

# Testing products endpoint
def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200  # Expecting a successful response
    assert isinstance(response.json(), list)  # Expecting a list of products

# Run the tests when executing file
if __name__ == "__main__":
    test_read_root()
    test_get_products()
    print("All tests successful!")



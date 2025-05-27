import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestUsers(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client for FastAPI.
        """
        self.client = TestClient(app)

    def test_user_registration(self):
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword"
        }
        response = self.client.post("/users/register", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], user_data["username"])

    def test_user_login(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        self.client.post("/users/register", json=user_data)
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post("/users/token", data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_user_login_incorrect_password(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        self.client.post("/users/register", json=user_data)
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post("/users/token", data=login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Incorrect username or password")

    def test_user_login_nonexistent_user(self):
        login_data = {
            "username": "nonexistent",
            "password": "password"
        }
        response = self.client.post("/users/token", data=login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Incorrect username or password")

if __name__ == "__main__":
    unittest.main()
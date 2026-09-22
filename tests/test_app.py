from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app, activities


client = TestClient(app)


def reset_state():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]


def test_signup_rejects_duplicate_email():
    reset_state()

    response = client.post("/activities/Chess Club/signup?email=daniel@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_participant_unregisters_them():
    reset_state()

    response = client.delete("/activities/Chess Club/participants?email=daniel@mergington.edu")

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"

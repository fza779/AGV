from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PathPlanningApiTests(APITestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("fza-health"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ready")

    def test_path_planning_endpoint(self):
        payload = {
            "grid": [
                [0, 0, 0],
                [1, 1, 0],
                [0, 0, 0],
            ],
            "start": [0, 0],
            "goal": [2, 2],
            "allow_diagonal": False,
        }

        response = self.client.post(reverse("path-plan"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["path"][0], [0, 0])
        self.assertEqual(response.data["path"][-1], [2, 2])
        self.assertEqual(response.data["cost"], 4.0)

    def test_invalid_grid_is_rejected(self):
        payload = {
            "grid": [
                [0, 0],
                [0],
            ],
            "start": [0, 0],
            "goal": [1, 0],
        }

        response = self.client.post(reverse("path-plan"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

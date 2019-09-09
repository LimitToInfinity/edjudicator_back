from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import HighScore
from .serializers import HighScoreSerializer
from .serializers import TokenSerializer
import simplejson as json

# Tests for views.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_high_score(value=-1):
        if value != -1:
            HighScore.objects.create(value=value)

    def login_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={"version": "v1"}
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    "username": username,
                    "password": password
                }
            ),
            content_type="application/json"
        )
        self.token = response.data["token"]
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def setUp(self):
        # create an admin user
        self.user = User.objects.create_superuser(
            username="testtt_alwaysss",
            email="i@madethisup.com",
            password="youknowit",
            first_name="testtt",
            last_name="alwaysss"
        )
        # add test data
        self.create_high_score(3)
        self.create_high_score(127)
        self.create_high_score(946)
        self.create_high_score(1149)

class GetAllHighScoresTest(BaseViewTest):
    
    def test_get_all_high_scores(self):
        """
        This test ensures all high scores added in the
        setUp method exist when we make a GET request to
        the highscores/ endpoint.
        """
        self.login_client("testtt_alwaysss", "youknowit")
        # hit the API endpoint
        response = self.client.get(
            reverse("high-scores-all",
            kwargs={"version": "v1"})
        )
        # fetch the data from the db
        expected = HighScore.objects.all()
        serialized = HighScoreSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint.
    """
    def test_login_user_with_valid_credentials(self):
        response = self.login_user("testtt_alwaysss", "youknowit")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED  )
        
    def test_login_user_with_invalid_credentials(self):
        response = self.login_user("fake", "lies")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint.
    """
    def test_register_user_with_valid_data(self):
        url = reverse(
            "auth-register",
            kwargs={"version": "v1"}
        )
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "lets_go_user",
                    "password": "lets_go_pass",
                    "email": "lets@go.com"
                }
            ),
            content_type="application/json"
        )
        # assert status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_data(self):
        url = reverse(
            "auth-register",
            kwargs={"version": "v1"}
        )
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "",
                    "password": "",
                    "email": ""
                }
            ),
            content_type="application/json"
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

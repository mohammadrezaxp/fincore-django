"""Django tests for FinCore project."""

from django.test import SimpleTestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class FinCoreSmokeTests(SimpleTestCase):
    """Test existing public page routes and status codes."""

    def test_routes(self):
        routes = [
            ("/", 200),
            ("/accounts/login/", 200),
            ("/accounts/register/", 200),
        ]
        for path, expected_status in routes:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, expected_status)

    def test_templates(self):
        """Test that root routes render valid templates."""
        response = self.client.get("/")
        if response.status_code == 200:
            self.assertContains(response, "FinCore", status_code=200)

        response = self.client.get("/accounts/login/")
        if response.status_code == 200:
            self.assertContains(response, "Log in", status_code=200)

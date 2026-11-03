from django.test import RequestFactory, SimpleTestCase

from accounts import views


class CustomErrorPageTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_403_page_returns_forbidden_status(self):
        request = self.factory.get("/restricted/")
        response = views.error_403(request)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "403", status_code=403)

    def test_404_page_returns_not_found_status(self):
        request = self.factory.get("/missing/")
        response = views.error_404(request)
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "404", status_code=404)

    def test_500_page_returns_generic_server_error(self):
        request = self.factory.get("/failure/")
        response = views.error_500(request)
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Something went wrong", status_code=500)
        self.assertNotContains(response, "Traceback")

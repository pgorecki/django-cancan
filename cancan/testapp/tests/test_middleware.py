from django.test import TestCase, Client, override_settings
from cancan.testapp.models import Article, User
from cancan.ability import Ability, AccessRules


def get_abilities(user, rules):
    rules.allow("view", Article, is_published=True)


@override_settings(
    CANCAN={"ABILITIES": "cancan.testapp.tests.test_middleware.get_abilities"}
)
class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.article1 = Article.objects.create(is_published=True)
        self.article2 = Article.objects.create(is_published=False)

    def test_list_view(self):
        c = Client()
        response = c.get("/articles/")
        ids = response.content.decode().split(" ")
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.article1.id), ids)
        self.assertNotIn(str(self.article2.id), ids)

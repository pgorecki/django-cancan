from django.test import TestCase
from cancan.testapp.models import Article, User
from cancan.ability import Ability


class ModelAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        # Article.objects.create(name="Hello", is_published=True)
        # Article.objects.create(name="World", is_published=False)

    def test_no_abilities_when_initialized(self):
        ability = Ability(user=self.user)
        self.assertFalse(ability.is_able_to('view', Article))

    def test_happy_path(self):
        ability = Ability(user=self.user)
        ability.can('view', Article)
        self.assertTrue(ability.is_able_to('view', Article))

    def test_unknown_name(self):
        ability = Ability(user=self.user)
        ability.can('view', Article)
        self.assertFalse(ability.is_able_to('read', Article))


class ObjectAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.ability = Ability(user=self.user)
        self.ability.can('view', Article, is_published=True)

    def test_can_view_published(self):
        article = Article.objects.create(name='test', is_published=True)
        self.assertTrue(self.ability.is_able_to(
            'view', article))

    def test_cannot_view_unpublished(self):
        article = Article.objects.create(name='test', is_published=False)
        self.assertFalse(self.ability.is_able_to(
            'view', article))

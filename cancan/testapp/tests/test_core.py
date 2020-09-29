from django.test import TestCase
from cancan.testapp.models import Article, User
from cancan.ability import Ability
from cancan.access_rules import AccessRules


class NoAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")

    def test_no_abilities_can_model(self):
        access_rules = AccessRules(user=self.user)
        ability = Ability(access_rules)
        self.assertFalse(ability.can("view", Article))

    def test_no_abilities_can_object(self):
        access_rules = AccessRules(user=self.user)
        ability = Ability(access_rules)
        article = Article.objects.create(name="foobar")
        self.assertFalse(ability.can("view", article))

    def test_no_abilities_queryset_for(self):
        access_rules = AccessRules(user=self.user)
        ability = Ability(access_rules)
        self.assertEqual(ability.queryset_for("view", Article).count(), 0)


class ModelAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")

    def test_no_abilities_when_initialized(self):
        access_rules = AccessRules(user=self.user)
        ability = Ability(access_rules)
        self.assertFalse(ability.can("view", Article))

    def test_happy_path(self):
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article)
        ability = Ability(access_rules)
        self.assertTrue(ability.can("view", Article))

    def test_unknown_name(self):
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article)
        ability = Ability(access_rules)
        self.assertFalse(ability.can("read", Article))


class ObjectAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article, is_published=True)
        self.ability = Ability(access_rules)

    def test_can_view_published(self):
        article = Article.objects.create(name="test", is_published=True)
        self.assertTrue(self.ability.can("view", article))

    def test_cannot_view_unpublished(self):
        article = Article.objects.create(name="test", is_published=False)
        self.assertFalse(self.ability.can("view", article))

    def test_get_queryset1(self):
        article1 = Article.objects.create(name="test", is_published=True)
        qs = self.ability.queryset_for("view", Article)
        self.assertEqual(qs.count(), 1)

    def test_get_queryset2(self):
        article1 = Article.objects.create(name="test", is_published=False)
        qs = self.ability.queryset_for("view", Article)
        self.assertEqual(qs.count(), 0)


class ObjectAbilitiesMultipleCanTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article, is_published=True)
        access_rules.allow("view", Article, created_by=self.user)
        self.ability = Ability(access_rules)

    def test_can_view_published(self):
        article1 = Article.objects.create(name="test", is_published=True)
        article2 = Article.objects.create(name="test", created_by=self.user)
        self.assertTrue(self.ability.can("view", article1))
        self.assertTrue(self.ability.can("view", article2))

    def test_queryset_contails_all_allowed(self):
        article1 = Article.objects.create(name="test", is_published=True)
        article2 = Article.objects.create(name="test", created_by=self.user)
        article3 = Article.objects.create(name="test", is_published=False)
        qs = self.ability.queryset_for("view", Article)
        self.assertEqual(qs.count(), 2)
        self.assertFalse(article3 in qs.all())


class AliasesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        article1 = Article.objects.create(name="test")
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article)
        access_rules.alias_action("view", "list")
        self.ability = Ability(access_rules)

    def test_can_view_published(self):
        self.assertTrue(self.ability.can("list", Article))
        self.assertEqual(self.ability.queryset_for("list", Article).count(), 1)


class MiscTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")
        article1 = Article.objects.create(name="test")
        access_rules = AccessRules(user=self.user)
        access_rules.allow("view", Article)
        access_rules.alias_action("view", "list")
        self.ability = Ability(access_rules)

    def test_in_operator(self):
        self.assertTrue(("view", Article) in self.ability)

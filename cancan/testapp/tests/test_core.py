from django.test import TestCase
from cancan.testapp.models import Article, User
from cancan.ability import Ability, AbilityValidator


class NoAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")

    def test_no_abilities_can_model(self):
        ability = Ability(user=self.user)
        validator = AbilityValidator(ability)
        self.assertFalse(validator.can('view', Article))

    def test_no_abilities_can_object(self):
        ability = Ability(user=self.user)
        validator = AbilityValidator(ability)
        article = Article.objects.create(name="foobar")
        self.assertFalse(validator.can('view', article))

    def test_no_abilities_queryset_for(self):
        ability = Ability(user=self.user)
        validator = AbilityValidator(ability)
        self.assertEqual(validator.queryset_for('view', Article).count(), 0)


class ModelAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")

    def test_no_abilities_when_initialized(self):
        ability = Ability(user=self.user)
        validator = AbilityValidator(ability)
        self.assertFalse(validator.can('view', Article))

    def test_happy_path(self):
        ability = Ability(user=self.user)
        ability.can('view', Article)
        validator = AbilityValidator(ability)
        self.assertTrue(validator.can('view', Article))

    def test_unknown_name(self):
        ability = Ability(user=self.user)
        ability.can('view', Article)
        validator = AbilityValidator(ability)
        self.assertFalse(validator.can('read', Article))


class ObjectAbilitiesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        ability = Ability(user=self.user)
        ability.can('view', Article, is_published=True)
        self.validator = AbilityValidator(ability)

    def test_can_view_published(self):
        article = Article.objects.create(name='test', is_published=True)
        self.assertTrue(self.validator.can(
            'view', article))

    def test_cannot_view_unpublished(self):
        article = Article.objects.create(name='test', is_published=False)
        self.assertFalse(self.validator.can(
            'view', article))

    def test_get_queryset1(self):
        article1 = Article.objects.create(name='test', is_published=True)
        qs = self.validator.queryset_for('view', Article)
        self.assertEqual(qs.count(), 1)

    def test_get_queryset2(self):
        article1 = Article.objects.create(name='test', is_published=False)
        qs = self.validator.queryset_for('view', Article)
        self.assertEqual(qs.count(), 0)


class ObjectAbilitiesMultipleCanTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        ability = Ability(user=self.user)
        ability.can('view', Article, is_published=True)
        ability.can('view', Article, created_by=self.user)
        self.validator = AbilityValidator(ability)

    def test_can_view_published(self):
        article1 = Article.objects.create(name='test', is_published=True)
        article2 = Article.objects.create(name='test', created_by=self.user)
        self.assertTrue(self.validator.can('view', article1))
        self.assertTrue(self.validator.can('view', article2))

    def test_queryset_contails_all_allowed(self):
        article1 = Article.objects.create(name='test', is_published=True)
        article2 = Article.objects.create(name='test', created_by=self.user)
        article3 = Article.objects.create(name='test', is_published=False)
        qs = self.validator.queryset_for('view', Article)
        self.assertEqual(qs.count(), 2)
        self.assertFalse(article3 in qs.all())


class AliasesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        article1 = Article.objects.create(name='test')
        ability = Ability(user=self.user)
        ability.can('view', Article)
        ability.set_alias('list', 'view')
        self.validator = AbilityValidator(ability)

    def test_can_view_published(self):
        self.assertTrue(self.validator.can('list', Article))
        self.assertEqual(self.validator.queryset_for(
            'list', Article).count(), 1)

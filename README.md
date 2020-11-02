# django-cancan

<p align="center">
    <img src="django-cancan.svg" alt="Logo" height="224" />
</p>

[![Build Status](https://travis-ci.com/pgorecki/django-cancan.svg?branch=master)](https://travis-ci.com/pgorecki/django-cancan)
[![PyPI version](https://badge.fury.io/py/django-cancan.svg)](https://badge.fury.io/py/django-cancan)

`django-cancan` is an authorization library for Django. It works on top of default Django permissions and allows to restrict the resources (models and objects) a given user can access.

This library is inspired by [cancancan](https://github.com/CanCanCommunity/cancancan) for Ruby on Rails.

## Key features

- All of your permissions logic is kept in one place. User permissions are defined in a single function and not scattered across views,
  querysets, etc.

- Same permissions logic is used to check permissions on a single model instance and to generate queryset containing all instances that the user can access

- Easy unit testing

- Integration with built-in Django default permissions system and Django admin (coming soon)

- Intergration with Django Rest Framework (coming soon)

## How to install

Using `pip`:

```
pip install django-cancan
```

## Quick start

1. Add `cancan` to your `INSTALLED_APPS` setting like this:

```python
INSTALLED_APPS = [
    ...,
    'cancan',
]
```

2. Create a function that define the access rules for a given user. For example, create `abilities.py` in `myapp` module:

```python
def define_access_rules(user, rules):
    # Anybody can view published articles
    rules.allow('view', Article, published=True)

    if not user.is_authenticated:
        return 

    # Allow logged in user to view his own articles, regardless of the `published` status
    # allow accepts the same kwargs that you would provide to QuerySet.filter method
    rules.allow('view', Article, author=user)

    if user.has_perm('article.view_unpublished'):
        # You can also check for custom model permissions (i.e. view_unpublished)
        rules.allow('view', Article, published=False)
    

    if user.is_superuser:
        # Superuser gets unlimited access to all articles
        rules.allow('add', Article)
        rules.allow('view', Article)
        rules.allow('change', Article)
        rules.allow('delete', Article)
```

3.  In `settings.py` add `CANCAN` section, so that `cancan` library will know where to search for `define_access_rules` function from the previous step:

```python
CANCAN = {
    'ABILITIES': 'myapp.abilities.define_access_rules'
}
```

The `define_access_rules` function will be executed automatically per each request by the `cancan` middleware. The middleware will call the function to determine the abilities of a current user.

Let's add `cancan` middleware, just after `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cancan.middleware.CanCanMiddleware',
    ...
]
```

By adding the middleware you will also get an access to `request.ability` instance which you can use
to: 
 - check model permissions, 
 - check object permissions,
 - generate model querysets (i.e. when inheriting from `ListView`)

4. Check for abilities in views:

```python

class ArticleListView(ListView):
    model = Article

    def get_queryset():
        # this is how you can retrieve all objects that current user can access
        qs = self.request.ability.queryset_for('view', Article)
        return qs


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    queryset = Article.objects.all()

    def has_permission(self):
        article = self.get_object()
        # this is how you can check if user can access an object
        return self.request.ability.can('view', article)
```

5. Check for abilities in templates

You can also check for abilities in template files, i. e. to show/hide/disable buttons or links.

First you need to add `cancan` processor to `context_processors` in `TEMPLATES` section of `settings.py`:

```python
TEMPLATES = [
    {
        ...,
        "OPTIONS": {
            "context_processors": [
                ...,
                "cancan.context_processors.abilities",
            ],
        },
    },
]
```

This will give you access to `ability` object in a template. You also need add `{% load cancan_tags %}` at the beginning 
of the template file.

Next you can check for object permissions:

```
{% load cancan_tags %}

...

{% if ability|can:"change"|subject:article %}
    <a href="{% url 'article_edit' pk=article.id %}">Edit article</a>
{% endif %}
```

or model permissions:

```
{% if ability|can:"add"|"myapp.Article" %}
    <a href="{% url 'article_new' %}">Create new article</a>
{% endif %}
```

You can also use `can` template tag to create a reusable variable:

```
{% can "add" "core.Project" as can_add_project %}
...
{% if can_add_project %}
    ...
{% endif %}
```

## Checking for abilities in Django Rest Framework

Let's start by creating a pemission class:

```python
from rest_framework import permissions

def set_aliases_for_drf_actions(ability):
    """
    map DRF actions to default Django permissions
    """
    ability.access_rules.alias_action("list", "view")
    ability.access_rules.alias_action("retrieve", "view")
    ability.access_rules.alias_action("create", "add")
    ability.access_rules.alias_action("update", "change")
    ability.access_rules.alias_action("partial_update", "change")
    ability.access_rules.alias_action("destroy", "delete")


class AbilityPermission(permissions.BasePermission):
    def has_permission(self, request, view=None):
        ability = request.ability
        set_aliases_for_drf_actions(ability)
        return ability.can(view.action, view.get_queryset().model)

    def has_object_permission(self, request, view, obj):
        ability = request.ability
        set_aliases_for_drf_actions(ability)
        return ability.can(view.action, obj)
```

Next, secure the ViewSet with `AbilityPermission` and override `get_queryset` method to list objects based on the access rights.

```python
class ArticleViewset(ModelViewSet):
    permission_classes = [AbilityPermission]

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Article).distinct()
```

## `ability.queryset_for` and `rules.allow` explained

When executing `rules.allow` you specify 2 positional arguments: `action` and `subject`. Any additional parameters passed to allow will filter
the results in the same way as for Django `QuerySet.fiter` method.

Let's say that we have the following models in `core.models.py`:

```python
class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(default="", blank=True)
    members = models.ManyToManyField(User, through="Membership")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
```

If you have the following rules:
```
rules.allow('view', Project, name="Foo")
```

then executing:
```
ability.queryset_for('view', Project)
```

will result in the following query:
```
SELECT "core_project"."id", "core_project"."name", "core_project"."description", "core_project"."created_by_id" FROM "core_project" WHERE "core_project"."name" = Foo
```

Similarly, `rules.allow('view', Project, name="Foo", description__contains="Bar")`

will generate a query:
```
SELECT "core_project"."id", "core_project"."name", "core_project"."description", "core_project"."created_by_id" FROM "core_project" WHERE ("core_project"."description" LIKE %Bar% ESCAPE '\' AND "core_project"."name" = Foo)
```

Multiple rules for the same action and model will result in OR'ed queries, i.e.:
```
rules.allow('view', Project, name="Foo")
rules.allow('view', Project, description__contains="Bar")
```

will generate a query:
```
SELECT "core_project"."id", "core_project"."name", "core_project"."description", "core_project"."created_by_id" FROM "core_project" WHERE ("core_project"."description" LIKE %Bar% ESCAPE '\' OR "core_project"."name" = Foo)
```

See [example_project/cancan_playground.ipynb](example_project/cancan_playground.ipynb) for more examples.


## Sponsors

<a href="https://ermlab.com/" target="_blank">
  <img src="https://ermlab.com/wp-content/uploads/2019/08/ermlab_logo_plain_h80.png" alt="Ermlab" width="200"/>
</a>

<hr>

<div>Logo made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

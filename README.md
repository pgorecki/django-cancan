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

2. Create a function that define user abilites. For example, in `abilities.py`:

```python
def declare_abilities(user, ability):
    if not user.is_authenticated:
        # Allow anonymous users to view published articles
        return ability.can('view', Article, published=True)

    if user.has_perm('article.view_own_article'):
        # Allow logged in user to change his articles
        return ability.can('change', Article, author=user)

    if user.is_superuser:
        # Allow superuser change all articles
        return ability.can('change', Article)
```

3. Configure `cancan` by adding `CANCAN` section in `settings.py`:

```python
CANCAN = {
    'ABILITIES': 'myapp.abilities.declare_abilities'
}
```

Next, add `cancan` middleware after `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cancan.middleware.CanCanMiddleware',
    ...
]
```

Adding the middleware adds `request.ability` instance which you can use
to check for: model permissions, object permissions and model querysets.

4. Check abilities in views:

```python

class ArticleListView(ListView):
    model = Article

    def get_queryset():
        # this is how you can retrieve all objects a user can access
        qs = self.request.ability.queryset_for('view', Article)
        return qs


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    queryset = Article.objects.all()

    def has_permission(self):
        article = self.get_object()
        # this is how you can check if user can access an object
        return self.request.ability.can('view', article)
```

## Sponsors

<a href="https://ermlab.com/" target="_blank">
  <img src="https://ermlab.com/wp-content/uploads/2019/08/ermlab_logo_plain_h80.png" alt="Ermlab" width="200"/>
</a>

<hr>

<div>Logo made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

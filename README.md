# django-cancan

`django-cancan` is an authorization library for Django. It works on top of default Django permissions and allows to restrict the resources (models and objects) a given user can access.

This library is inspired by [cancancan](https://github.com/CanCanCommunity/cancancan) for Ruby on Rails.

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

    def get_query_set():
        # this is how you can retrieve all objects a user can access
        qs = self.request.ability.query_set_for('view', Article)
        return qs


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    queryset = Article.objects.all()

    def has_permission(self):
        article = self.get_object()
        # this is how you can check if user can access an object
        return self.request.ability.can('view', article)
```

## Testing

Run `./manage.py test` to run all test for the `testapp`

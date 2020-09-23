from django import template
from django.apps import apps
from django.utils.safestring import SafeString

register = template.Library()


@register.simple_tag(takes_context=True)
def can(context, action, subject):
    is_allowed = False
    if type(subject) is SafeString:
        model = apps.get_model(subject)
        print(model)
        is_allowed = context["request"].ability.can(action, model)
    return f"can {action} {subject}? {is_allowed}"

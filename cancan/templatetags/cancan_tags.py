from django import template
from django.apps import apps
from django.utils.safestring import SafeString
from cancan.access_rules import normalize_subject

register = template.Library()


@register.filter
def can(abilities, action):
    matching_rules = list(filter(lambda rule: rule['action'] == action, abilities))
    return matching_rules

@register.filter
def subject(abilities, subject):
    s = normalize_subject(str(subject))
    matching_rules = list(filter(lambda rule: rule['model'] == s, abilities))
    return matching_rules

@register.simple_tag(takes_context=True)
def can(context, action, subject):
    is_allowed = False
    if type(subject) is SafeString:
        model = apps.get_model(subject)
        print(model)
        is_allowed = context["request"].ability.can(action, model)
    return f"can {action} {subject}? {is_allowed}"

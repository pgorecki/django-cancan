from django import template
from django.apps import apps
from django.utils.safestring import SafeString
from cancan.ability import Ability

register = template.Library()


class AbilityCheck:
    """
    This function is used internally to check for ability within a template i. e.
    {% if ability|can:"view"|subject:project %}
        <a href="#" class="card-footer-item">View</a>
    {% endif %}
    """

    def __init__(self, ability):
        self.ability = ability
        self.action = None
        self.subject = None

    def __repr__(self):
        return f"{self.ability}(action={self.action},subject={self.subject})"

    def __bool__(self):
        return self.ability.can(self.action, self.subject)


@register.filter
def can(ability, action):
    if not isinstance(ability, AbilityCheck):
        assert isinstance(
            ability, Ability
        ), f"can filter must be applied to Ability instance (you provided {type(ability)})"
        ability = AbilityCheck(ability)
    ability.action = action
    return ability


@register.filter
def subject(ability, subject):
    if not isinstance(ability, AbilityCheck):
        assert isinstance(
            ability, Ability
        ), f"subject filter must be applied to Ability instance (you provided {type(ability)})"
        ability = AbilityCheck(ability)
    ability.subject = subject
    return ability


@register.simple_tag(takes_context=True)
def can(context, action, subject):
    return context["request"].ability.can(action, subject)

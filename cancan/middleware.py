from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from .ability import Ability, AbilityValidator


def get_validator(request, declare_abilities):
    ability = Ability(request.user)
    declare_abilities(request.user, ability)
    return AbilityValidator(ability)


class CanCanMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "Cancan authentication middleware requires authenticationMiddleware middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before."
            "'cancan.middleware.CanCanMiddleware'"
        )

        assert hasattr(settings, 'CANCAN'), (
            "CANCAN section not found in settings"
        )
        assert 'ABILITIES' in settings.CANCAN, (
            "CANCAN['ABILITIES'] is missing. It must point to a function"
        )
        fn_name = settings.CANCAN['ABILITIES']

        declare_abilities = import_string(settings.CANCAN['ABILITIES'])

        assert callable(declare_abilities), (
            f"{fn_name}  must be callabe function fn(user: User, ability: Ability)"
        )

        request.ability = SimpleLazyObject(
            lambda: get_validator(request, declare_abilities))

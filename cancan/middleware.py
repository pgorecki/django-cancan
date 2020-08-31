from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.module_loading import import_string

from .ability import Ability


class CanCanGoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "Cancango authentication middleware requires authenticationMiddleware middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before."
            "'cancango.middleware.CanCanGoMiddleware'"
        )

        assert hasattr(settings, 'CANCANGO'), (
            "CANCANGO section not found in settings"
        )
        assert 'ABILITIES' in settings.CANCANGO, (
            "CANCANGO['ABILITIES'] is missing. It must point to a function"
        )
        fn_name = settings.CANCANGO['ABILITIES']

        declare_abilities = import_string(settings.CANCANGO['ABILITIES'])

        assert callable(declare_abilities), (
            f"{fn_name}  must be callabe function fn(user: User, ability: Ability)"
        )

        ability = Ability(request.user)
        declare_abilities(request.user, ability)

        def can(action, model_or_instance):
            print(action, model_or_instance)
            return ability.is_able_to(action, model_or_instance)

        request.user.can = can

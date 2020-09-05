import inspect
from django.apps import apps


class Ability:
    def __init__(self, user):
        self.user = user
        self.abilities = []
        self.aliases = {}

    def can(self, action, model, **kwargs):
        if type(model) is str:
            model = apps.get_model(model)
        self.abilities.append({
            'type': 'can',
            'action': action,
            'model': model,
            'conditions': kwargs,
        })

    def cannot(self, action, model, **kwargs):
        if type(model) is str:
            model = apps.get_model(model)

        self.abilities.append({
            'type': 'cannot',
            'action': action,
            'model': model,
            'conditions': kwargs,
        })

    def set_alias(self, alias, action):
        self.aliases[alias] = action

    def alias_to_action(self, alias):
        return self.aliases.get(alias, alias)


class AbilityValidator:
    def __init__(self, ability: Ability):
        self.ability = ability

    def validate_model(self, action, model):
        can_count = 0
        cannot_count = 0
        model_abilities = filter(
            lambda c: c['model'] == model and c['action'] == action, self.ability.abilities)
        for c in model_abilities:
            if c['type'] == 'can':
                can_count += 1
            if c['type'] == 'cannot':
                cannot_count += 1

        if cannot_count > 0:
            return False
        if can_count == 0:
            return False
        return True

    def validate_instance(self, action, instance):
        model = instance._meta.model
        model_abilities = filter(
            lambda c: c['model'] == model and c['action'] == action, self.ability.abilities)

        query_sets = []
        for c in model_abilities:
            if c['type'] == 'can':
                qs = model.objects.all().filter(pk=instance.id, **c.get('conditions', {}))

            if c['type'] == 'cannot':
                raise NotImplementedError(
                    'cannot-type rules are not yet implemented')

            query_sets.append(qs)

        if len(query_sets) == 0:
            return False

        can_query_set = query_sets.pop()
        for qs in query_sets:
            can_query_set |= qs

        return can_query_set.count() > 0

    def can(self, action, model_or_instance) -> bool:
        action = self.ability.alias_to_action(action)
        if inspect.isclass(model_or_instance):
            return self.validate_model(action, model_or_instance)
        else:
            return self.validate_instance(action, model_or_instance)

    def queryset_for(self, action, model):
        action = self.ability.alias_to_action(action)

        model_abilities = filter(
            lambda c: c['model'] == model and c['action'] == action, self.ability.abilities)

        query_sets = []
        for c in model_abilities:
            if c['type'] == 'can' and 'conditions' in c:
                qs = model.objects.all().filter(**c.get('conditions', {}))

            if c['type'] == 'cannot':
                raise NotImplementedError(
                    'cannot-type rules are not yet implemented')

            query_sets.append(qs)

        if len(query_sets) == 0:
            return model.objects.none()

        can_query_set = query_sets.pop()
        for qs in query_sets:
            can_query_set |= qs

        return can_query_set

from django.apps import apps


def normalize_subject(subject):
    if isinstance(subject, str):
        try:
            app_label, model_name = subject.split(".")
            return apps.get_model(app_label, model_name)
        except Exception as e:
            pass
    return subject


class AccessRules:
    def __init__(self, user):
        self.user = user
        self.rules = []
        self.action_aliases = {}

    def allow(self, action, subject, **kwargs):
        rule = {
            "type": "can",
            "action": action,
            "subject": normalize_subject(subject),
            "conditions": kwargs,
        }
        self.rules.append(rule)
        return rule

    def alias_action(self, action, alias):
        self.action_aliases[alias] = action

    def alias_to_action(self, alias):
        return self.action_aliases.get(alias, alias)

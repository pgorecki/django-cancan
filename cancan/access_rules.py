class AccessRules:
    def __init__(self, user):
        self.user = user
        self.rules = []
        self.action_aliases = {}

    def allow(self, action, subject, **kwargs):
        if type(subject) is str:
            model = apps.get_model(subject)
        rule = {
            "type": "can",
            "action": action,
            "model": subject,
            "conditions": kwargs,
        }
        self.rules.append(rule)
        return rule

    def alias_action(self, action, alias):
        self.action_aliases[alias] = action

    def alias_to_action(self, alias):
        return self.action_aliases.get(alias, alias)
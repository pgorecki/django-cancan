def abilities(request):
    return {"abilities": request.ability.access_rules.rules}

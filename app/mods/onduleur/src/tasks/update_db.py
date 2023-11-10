from src.memo import memo

def update_db():
    if memo["onduleurs_data"].isReady():
        memo["onduleurs_data"].majAllDataBdd(_timeout=100)
    else:
        memo["onduleurs_data"].ajouterOnduleurs(_timeout=10)
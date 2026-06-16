import unicodedata

def nettoyer_et_analyser_nom(nom_brut):
    if not nom_brut:
        return "", []

    # 1. Retirer les accents et mettre en minuscule
    nom_nettoye = unicodedata.normalize('NFKD', nom_brut).encode('ASCII', 'ignore').decode('utf-8')

    # 2. Remplacer les tirets et underscores par des espaces
    nom_nettoye = nom_nettoye.replace('-', ' ').replace('_', ' ')

    # 3. Nettoyer les espaces multiples et mettre en majuscule proprement (ex: Jean Michel)
    mots = [mot.capitalize() for mot in nom_nettoye.split() if mot]
    nom_final = " ".join(mots)

    # 4. Générer des alternatives (si le nom contient plusieurs mots)
    alternatives = []
    if len(mots) >= 2:
        # Alternative 1 : Juste le premier mot
        alternatives.append(mots[0])
        # Alternative 2 : Juste le deuxième mot
        alternatives.append(mots[1])
        # Alternative 3 : Inverser les deux premiers mots
        alternatives.append(f"{mots[1]} {mots[0]}")

    return nom_final, alternatives

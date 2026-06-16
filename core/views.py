from django.shortcuts import render
from .models import CategorieMacro, Macro
from .utils import nettoyer_et_analyser_nom


def dashboard(request):
    """Page d'accueil avec les deux CTA et les KPI cards."""
    context = {}
    return render(request, 'core/dashboard.html', context)


def normaliser(request):
    """Normalisateur de noms clients."""
    nom_input = ""
    nom_clean = ""
    alternatives = []

    if request.method == "POST" and "nom_a_normaliser" in request.POST:
        nom_input = request.POST.get("nom_a_normaliser", "")
        nom_clean, alternatives = nettoyer_et_analyser_nom(nom_input)

    context = {
        'nom_input': nom_input,
        'nom_clean': nom_clean,
        'alternatives': alternatives,
    }
    return render(request, 'core/normaliser.html', context)


def wiki(request):
    """Wiki macros — interface 3 panneaux."""
    categories = CategorieMacro.objects.prefetch_related('macros').all()

    context = {
        'categories': categories,
    }
    return render(request, 'core/wiki.html', context)

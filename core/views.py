import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import CategorieMacro, Macro, Theme, Article
from .utils import nettoyer_et_analyser_nom


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def dashboard(request):
    return render(request, 'core/dashboard.html', {})


# ─────────────────────────────────────────────────────────────────────────────
# NORMALISATEUR
# ─────────────────────────────────────────────────────────────────────────────

def normaliser(request):
    nom_input = nom_clean = ""
    alternatives = []
    if request.method == "POST" and "nom_a_normaliser" in request.POST:
        nom_input = request.POST.get("nom_a_normaliser", "")
        nom_clean, alternatives = nettoyer_et_analyser_nom(nom_input)
    return render(request, 'core/normaliser.html', {
        'nom_input':    nom_input,
        'nom_clean':    nom_clean,
        'alternatives': alternatives,
    })


# ─────────────────────────────────────────────────────────────────────────────
# WIKI — page principale
# ─────────────────────────────────────────────────────────────────────────────

def wiki(request):
    categories       = CategorieMacro.objects.prefetch_related('macros').all()
    themes           = Theme.objects.prefetch_related('articles').all()
    articles_sans_theme = Article.objects.filter(theme__isnull=True).order_by('-date_modif')
    return render(request, 'core/wiki.html', {
        'categories':          categories,
        'themes':              themes,
        'articles_sans_theme': articles_sans_theme,
    })


# ─────────────────────────────────────────────────────────────────────────────
# WIKI — MACROS (AJAX)
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def creer_macro(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'JSON invalide.'}, status=400)

    titre   = data.get('titre',         '').strip()
    contenu = data.get('contenu',        '').strip()
    cat_id  = data.get('categorie_id',   '').strip()
    cat_nom = data.get('categorie_nom',  '').strip()

    if not titre:
        return JsonResponse({'success': False, 'error': 'Titre obligatoire.'}, status=422)
    if not contenu:
        return JsonResponse({'success': False, 'error': 'Contenu obligatoire.'}, status=422)
    if not cat_id and not cat_nom:
        return JsonResponse({'success': False, 'error': 'Catégorie requise.'}, status=422)

    if cat_id:
        try:
            categorie = CategorieMacro.objects.get(pk=int(cat_id))
        except (CategorieMacro.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'error': 'Catégorie introuvable.'}, status=404)
    else:
        categorie, _ = CategorieMacro.objects.get_or_create(nom=cat_nom)

    macro = Macro.objects.create(titre=titre, contenu=contenu, categorie=categorie)
    return JsonResponse({
        'success':       True,
        'macro_id':      macro.pk,
        'categorie_id':  categorie.pk,
        'categorie_nom': categorie.nom,
    }, status=201)


# ─────────────────────────────────────────────────────────────────────────────
# WIKI — ARTICLES (AJAX)
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def creer_article(request):
    """Crée un article (et optionnellement un thème). Body JSON."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'JSON invalide.'}, status=400)

    titre      = data.get('titre',       '').strip()
    contenu_md = data.get('contenu_md',  '').strip()
    resume     = data.get('resume',      '').strip()
    theme_id   = data.get('theme_id',    '').strip()
    theme_nom  = data.get('theme_nom',   '').strip()

    if not titre:
        return JsonResponse({'success': False, 'error': 'Titre obligatoire.'}, status=422)
    if not contenu_md:
        return JsonResponse({'success': False, 'error': 'Contenu obligatoire.'}, status=422)

    theme = None
    if theme_id:
        try:
            theme = Theme.objects.get(pk=int(theme_id))
        except (Theme.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'error': 'Thème introuvable.'}, status=404)
    elif theme_nom:
        theme, _ = Theme.objects.get_or_create(nom=theme_nom)

    article = Article.objects.create(
        titre=titre, contenu_md=contenu_md,
        resume=resume, theme=theme
    )
    return JsonResponse({
        'success':    True,
        'article_id': article.pk,
        'theme_id':   theme.pk   if theme else None,
        'theme_nom':  theme.nom  if theme else None,
    }, status=201)


def lire_article(request, article_id):
    """Retourne le contenu Markdown d'un article en JSON."""
    article = get_object_or_404(Article, pk=article_id)
    return JsonResponse({
        'id':           article.pk,
        'titre':        article.titre,
        'contenu_md':   article.contenu_md,
        'resume':       article.get_resume(),
        'theme_id':     article.theme_id,
        'theme_nom':    article.theme.nom if article.theme else '',
        'date_modif':   article.date_modif.strftime('%d/%m/%Y'),
        'date_creation':article.date_creation.strftime('%d/%m/%Y'),
    })


@require_http_methods(["POST"])
def modifier_article(request, article_id):
    """Met à jour titre + contenu_md d'un article. Body JSON."""
    article = get_object_or_404(Article, pk=article_id)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'JSON invalide.'}, status=400)

    article.titre      = data.get('titre',      article.titre).strip() or article.titre
    article.contenu_md = data.get('contenu_md', article.contenu_md).strip() or article.contenu_md
    article.resume     = data.get('resume',     article.resume).strip()
    article.save()
    return JsonResponse({'success': True, 'article_id': article.pk})


@require_http_methods(["POST"])
def supprimer_article(request, article_id):
    """Supprime un article."""
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return JsonResponse({'success': True})

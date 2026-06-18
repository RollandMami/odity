from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ── Dashboard ──────────────────────────────────────────────
    path('',                            views.dashboard,        name='dashboard'),
    # ── Normalisateur ──────────────────────────────────────────
    path('normaliser/',                 views.normaliser,       name='normaliser'),
    # ── Wiki — page principale ─────────────────────────────────
    path('wiki/',                       views.wiki,             name='wiki'),
    # ── Wiki — Macros (AJAX) ───────────────────────────────────
    path('wiki/macro/creer/',           views.creer_macro,      name='creer_macro'),
    # ── Wiki — Articles (AJAX) ────────────────────────────────
    path('wiki/article/creer/',         views.creer_article,    name='creer_article'),
    path('wiki/article/<int:article_id>/',          views.lire_article,     name='lire_article'),
    path('wiki/article/<int:article_id>/modifier/', views.modifier_article, name='modifier_article'),
    path('wiki/article/<int:article_id>/supprimer/',views.supprimer_article,name='supprimer_article'),
]

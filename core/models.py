from django.db import models


# ── MACROS ────────────────────────────────────────────────────────────────────

class CategorieMacro(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Catégorie de macro"
        verbose_name_plural = "Catégories de macros"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Macro(models.Model):
    titre     = models.CharField(max_length=200)
    categorie = models.ForeignKey(
        CategorieMacro, on_delete=models.CASCADE, related_name='macros'
    )
    contenu       = models.TextField(help_text="Le texte de la réponse type")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Macro"
        ordering = ['titre']

    def __str__(self):
        return self.titre


# ── WIKI / BASE DE CONNAISSANCES ───────────────────────────────────────────────

class Theme(models.Model):
    """Thème de regroupement des articles du wiki (ex: Onboarding, Réclamations…)."""
    nom         = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    icone       = models.CharField(
        max_length=60, blank=True, default='fa-folder',
        help_text="Classe Font Awesome, ex: fa-book"
    )
    ordre       = models.PositiveSmallIntegerField(default=0, help_text="Ordre d'affichage")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thème wiki"
        verbose_name_plural = "Thèmes wiki"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom


class Article(models.Model):
    """
    Article de la base de connaissances.
    Le contenu est stocké en Markdown et rendu côté client.
    """
    titre        = models.CharField(max_length=250)
    theme        = models.ForeignKey(
        Theme, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='articles'
    )
    contenu_md   = models.TextField(
        help_text="Contenu en Markdown (titres, listes, code, etc.)"
    )
    resume       = models.CharField(
        max_length=300, blank=True,
        help_text="Résumé court affiché dans la card d'accueil (auto-généré si vide)"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article wiki"
        verbose_name_plural = "Articles wiki"
        ordering = ['-date_modif']

    def __str__(self):
        return self.titre

    def get_resume(self):
        """Retourne le résumé ou les 150 premiers caractères du contenu."""
        if self.resume:
            return self.resume
        # Enlève les marqueurs Markdown basiques pour le résumé
        import re
        texte = re.sub(r'[#*`_>\[\]!]', '', self.contenu_md)
        return texte.strip()[:150]

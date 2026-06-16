from django.db import models

class CategorieMacro(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Macro(models.Model):
    titre = models.CharField(max_length=200)
    categorie = models.ForeignKey(CategorieMacro, on_delete=models.CASCADE, related_name='macros')
    contenu = models.TextField(help_text="Le texte de la réponse type")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

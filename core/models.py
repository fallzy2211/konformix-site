from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Lead(models.Model):
    """Une demande entrante : démo, contact ou téléchargement de ressource."""

    class Source(models.TextChoices):
        DEMO = "demo", _("Demande de démonstration")
        CONTACT = "contact", _("Contact général")
        RESOURCE = "resource", _("Téléchargement de ressource")

    class Interest(models.TextChoices):
        KONTROL = "kontrol", _("Fiabilisation des données KYC")
        VIGIL = "vigil", _("Profilage clients & transactions")
        BOTH = "both", _("Plusieurs modules")
        OTHER = "other", _("Autre besoin")

    full_name = models.CharField(_("nom complet"), max_length=150)
    email = models.EmailField(_("e-mail professionnel"))
    phone = models.CharField(_("téléphone"), max_length=40, blank=True)
    organisation = models.CharField(_("établissement"), max_length=150)
    job_title = models.CharField(_("fonction"), max_length=150, blank=True)
    country = models.CharField(_("pays"), max_length=80, blank=True)
    interest = models.CharField(
        _("centre d'intérêt"),
        max_length=20,
        choices=Interest.choices,
        default=Interest.BOTH,
    )
    message = models.TextField(_("message"), blank=True)
    source = models.CharField(
        _("origine"), max_length=20, choices=Source.choices, default=Source.DEMO
    )
    consent = models.BooleanField(_("consentement au traitement des données"), default=False)
    created_at = models.DateTimeField(_("reçu le"), default=timezone.now, editable=False)
    handled = models.BooleanField(_("traité"), default=False)
    internal_notes = models.TextField(_("notes internes"), blank=True)

    class Meta:
        verbose_name = _("demande entrante")
        verbose_name_plural = _("demandes entrantes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.organisation}"


class Article(models.Model):
    """Publication de la rubrique Ressources (veille réglementaire, notes techniques)."""

    class Category(models.TextChoices):
        REGULATION = "regulation", _("Veille réglementaire")
        METHOD = "method", _("Méthode & bonnes pratiques")
        PRODUCT = "product", _("Produit")
        CASE = "case", _("Retour d'expérience")

    title = models.CharField(_("titre"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=220, unique=True)
    category = models.CharField(
        _("catégorie"), max_length=20, choices=Category.choices, default=Category.REGULATION
    )
    excerpt = models.TextField(_("chapô"), max_length=400)
    body = models.TextField(_("contenu"), help_text=_("HTML simple accepté."))
    published_at = models.DateField(_("publié le"), default=timezone.localdate)
    is_published = models.BooleanField(_("en ligne"), default=False)
    reading_minutes = models.PositiveSmallIntegerField(_("durée de lecture (min)"), default=5)

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("article_detail", args=[self.slug])

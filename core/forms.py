from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Lead

COUNTRIES = [
    ("", _("Sélectionnez un pays")),
    ("SN", "Sénégal"),
    ("CI", "Côte d'Ivoire"),
    ("ML", "Mali"),
    ("BF", "Burkina Faso"),
    ("BJ", "Bénin"),
    ("TG", "Togo"),
    ("NE", "Niger"),
    ("GW", "Guinée-Bissau"),
    ("GN", "Guinée"),
    ("MR", "Mauritanie"),
    ("CM", "Cameroun"),
    ("GA", "Gabon"),
    ("CG", "Congo"),
    ("TD", "Tchad"),
    ("CF", "Centrafrique"),
    ("GQ", "Guinée équatoriale"),
    ("NG", "Nigeria"),
    ("GH", "Ghana"),
    ("OTHER", _("Autre")),
]


class LeadForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES, required=False, label=_("Pays"))

    # Champ piège anti-robot : invisible pour un humain, rempli par les bots.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = [
            "full_name",
            "email",
            "phone",
            "organisation",
            "job_title",
            "country",
            "interest",
            "message",
            "consent",
        ]
        labels = {
            "full_name": _("Nom et prénom"),
            "email": _("E-mail professionnel"),
            "phone": _("Téléphone"),
            "organisation": _("Établissement"),
            "job_title": _("Fonction"),
            "interest": _("Votre besoin"),
            "message": _("Votre message"),
            "consent": _(
                "J'accepte que mes données soient utilisées pour traiter ma demande."
            ),
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": _("Aminata Ndiaye"),
            "email": _("a.ndiaye@votrebanque.com"),
            "phone": _("+221 …"),
            "organisation": _("Nom de votre banque ou établissement"),
            "job_title": _("Directeur de la Conformité"),
            "message": _("Décrivez brièvement votre contexte et votre échéance."),
        }
        for name, field in self.fields.items():
            if name == "website":
                continue
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "checkbox")
            else:
                field.widget.attrs.setdefault("class", "field")
            if name in placeholders:
                field.widget.attrs.setdefault("placeholder", placeholders[name])

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(_("Requête invalide."))
        return ""

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise forms.ValidationError(
                _("Merci de confirmer votre accord pour que nous puissions vous répondre.")
            )
        return consent

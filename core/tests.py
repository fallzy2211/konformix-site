from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Article, Lead


class PublicPagesTests(TestCase):
    def test_all_public_pages_render(self):
        for name in ["home", "products", "about", "resources", "contact", "legal", "privacy"]:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Konformix")

    def test_product_detail_pages(self):
        for key in ["kontrol", "vigil"]:
            with self.subTest(product=key):
                response = self.client.get(reverse("product_detail", args=[key]))
                self.assertEqual(response.status_code, 200)

    def test_unknown_product_returns_404(self):
        response = self.client.get(reverse("product_detail", args=["inexistant"]))
        self.assertEqual(response.status_code, 404)

    def test_robots_and_sitemap(self):
        self.assertEqual(self.client.get("/robots.txt").status_code, 200)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)


class ArticleTests(TestCase):
    def setUp(self):
        self.published = Article.objects.create(
            title="Note publiée",
            slug="note-publiee",
            excerpt="Chapô.",
            body="<p>Corps.</p>",
            is_published=True,
        )
        self.draft = Article.objects.create(
            title="Brouillon",
            slug="brouillon",
            excerpt="Chapô.",
            body="<p>Corps.</p>",
            is_published=False,
        )

    def test_only_published_articles_are_listed(self):
        response = self.client.get(reverse("resources"))
        self.assertContains(response, "Note publiée")
        self.assertNotContains(response, "Brouillon")

    def test_draft_detail_is_not_reachable(self):
        self.assertEqual(
            self.client.get(reverse("article_detail", args=["brouillon"])).status_code, 404
        )
        self.assertEqual(
            self.client.get(reverse("article_detail", args=["note-publiee"])).status_code, 200
        )


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    LEAD_NOTIFICATION_EMAILS=["commercial@konformix.com"],
)
class LeadFormTests(TestCase):
    valid_payload = {
        "full_name": "Aminata Ndiaye",
        "email": "a.ndiaye@banque-test.sn",
        "phone": "+221770000000",
        "organisation": "Banque de Test",
        "job_title": "Directrice de la Conformité",
        "country": "SN",
        "interest": "both",
        "message": "Nous préparons une mission d'inspection.",
        "consent": "on",
        "source": "demo",
    }

    def test_valid_submission_creates_lead_and_notifies(self):
        response = self.client.post(reverse("contact"), self.valid_payload)
        self.assertEqual(response.status_code, 302)

        lead = Lead.objects.get()
        self.assertEqual(lead.organisation, "Banque de Test")
        self.assertEqual(lead.source, "demo")
        self.assertTrue(lead.consent)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Banque de Test", mail.outbox[0].subject)

    def test_consent_is_required(self):
        payload = dict(self.valid_payload)
        payload.pop("consent")
        response = self.client.post(reverse("contact"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        payload = dict(self.valid_payload, website="http://spam.example")
        response = self.client.post(reverse("contact"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_email_is_rejected(self):
        payload = dict(self.valid_payload, email="pas-un-email")
        self.client.post(reverse("contact"), payload)
        self.assertEqual(Lead.objects.count(), 0)


class BrandConfigurationTests(TestCase):
    @override_settings(
        BRAND={
            "name": "Testix",
            "legal_name": "Testix SUARL",
            "tagline": "Slogan de test.",
            "domain": "testix.com",
            "email": "contact@testix.com",
            "sales_email": "commercial@testix.com",
            "phone": "+221 00 000 00 00",
            "address": "Dakar, Sénégal",
            "linkedin": "",
            "founded": "2026",
            "products": {},
        }
    )
    def test_brand_name_is_driven_by_settings(self):
        """Changer le nom de la société ne doit demander qu'une seule modification."""
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Testix")


class TranslationTests(TestCase):
    """Le selecteur FR/EN doit reellement changer la langue du site."""

    def test_home_is_served_in_english(self):
        self.client.post(
            reverse("set_language"), {"language": "en", "next": reverse("home")}
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Your customer data is your first compliance risk.")
        self.assertContains(response, 'lang="en"')

    def test_home_stays_french_by_default(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Vos données clients sont votre premier risque")
        self.assertContains(response, 'lang="fr"')

    def test_catalog_has_no_untranslated_string(self):
        call_command("build_translations", "--check", stdout=StringIO())

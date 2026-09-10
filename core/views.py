from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from . import content
from .forms import LeadForm
from .models import Article, Lead


def _base_context(page, **extra):
    ctx = {
        "page": page,
        "products": content.PRODUCTS,
        **extra,
    }
    return ctx


def home(request):
    return render(
        request,
        "pages/home.html",
        _base_context(
            "home",
            hero=content.HERO,
            stats=content.TRUST_STATS,
            problem=content.PROBLEM,
            differentiators=content.DIFFERENTIATORS,
            audiences=content.AUDIENCES,
            steps=content.APPROACH_STEPS,
        ),
    )


def products(request):
    return render(
        request,
        "pages/products.html",
        _base_context("products", steps=content.APPROACH_STEPS),
    )


def product_detail(request, key):
    product = next((p for p in content.PRODUCTS if p["key"] == key), None)
    if product is None:
        raise Http404
    others = [p for p in content.PRODUCTS if p["key"] != key]
    return render(
        request,
        "pages/product_detail.html",
        _base_context("products", product=product, others=others, faq=content.FAQ),
    )


def about(request):
    return render(
        request,
        "pages/about.html",
        _base_context(
            "about",
            founders=content.FOUNDERS,
            differentiators=content.DIFFERENTIATORS,
        ),
    )


def resources(request):
    articles = Article.objects.filter(is_published=True)
    return render(
        request,
        "pages/resources.html",
        _base_context("resources", articles=articles),
    )


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related = Article.objects.filter(is_published=True).exclude(pk=article.pk)[:3]
    return render(
        request,
        "pages/article_detail.html",
        _base_context("resources", article=article, related=related),
    )


def contact(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.source = request.POST.get("source") or Lead.Source.DEMO
            lead.save()
            _notify_team(lead)
            messages.success(
                request,
                _(
                    "Merci, votre demande est enregistrée. Nous revenons vers vous "
                    "sous un jour ouvré."
                ),
            )
            return redirect(reverse("contact") + "?ok=1")
    else:
        form = LeadForm()

    return render(
        request,
        "pages/contact.html",
        _base_context("contact", form=form, faq=content.FAQ),
    )


def _notify_team(lead):
    """Envoie la notification interne. Échoue en silence : ne jamais perdre un lead."""
    recipients = getattr(settings, "LEAD_NOTIFICATION_EMAILS", [])
    if not recipients:
        return
    try:
        body = render_to_string("emails/lead_notification.txt", {"lead": lead})
        send_mail(
            subject=f"[{settings.BRAND['name']}] Nouvelle demande — {lead.organisation}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    except Exception:  # pragma: no cover - la notification ne doit jamais bloquer
        pass


def legal(request):
    return render(request, "pages/legal.html", _base_context("legal"))


def privacy(request):
    return render(request, "pages/privacy.html", _base_context("privacy"))


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def handler404(request, exception):  # pragma: no cover
    return render(request, "pages/404.html", _base_context("404"), status=404)

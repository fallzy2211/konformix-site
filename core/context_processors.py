from django.conf import settings


def brand(request):
    """Rend l'identité de marque disponible dans tous les templates."""
    return {"brand": settings.BRAND}

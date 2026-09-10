"""
Extraction et compilation des catalogues de traduction, sans GNU gettext.

`makemessages` / `compilemessages` de Django reposent sur les binaires xgettext
et msgfmt, absents des postes Windows. Cette commande fait le même travail en
Python pur : elle parcourt les sources, met a jour les fichiers .po existants en
conservant les traductions deja saisies, puis genere les .mo.
"""

from __future__ import annotations

import ast
import re
from datetime import datetime, timezone
from pathlib import Path

import polib
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

PY_DIRS = ("core", "config")
TEMPLATE_DIR = "templates"

# {% translate "texte" %} / {% trans "texte" %}
TRANS_TAG = re.compile(r"""{%\s*(?:translate|trans)\s+("|')(?P<msg>[^"']*?)\1""")
# {% blocktranslate [with ...] %}texte{% endblocktranslate %}
BLOCK_TAG = re.compile(
    r"{%\s*blocktranslate(?:\s[^%]*)?\s*%}(?P<msg>.*?){%\s*endblocktranslate\s*%}", re.S
)


class Command(BaseCommand):
    help = "Extrait les chaines traduisibles et compile les catalogues .mo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--locale",
            action="append",
            dest="locales",
            help="Langue a traiter (repetable). Defaut : toutes sauf la langue source.",
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="Echoue si une chaine est manquante ou non traduite, sans rien ecrire.",
        )

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR)
        entries = self.collect(base)
        self.stdout.write(f"{len(entries)} chaine(s) traduisible(s) trouvee(s).")

        source = settings.LANGUAGE_CODE
        locales = options["locales"] or [
            code for code, _label in settings.LANGUAGES if code != source
        ]
        if not locales:
            raise CommandError("Aucune langue cible a traiter.")

        missing_total = 0
        for code in locales:
            missing_total += self.sync(base, code, entries, check=options["check"])

        if options["check"] and missing_total:
            raise CommandError(f"{missing_total} chaine(s) sans traduction.")

    # -- extraction ---------------------------------------------------------

    def collect(self, base: Path) -> dict[str, list[str]]:
        """Renvoie {msgid: [occurrences "fichier:ligne"]}, ordre de decouverte."""
        found: dict[str, list[str]] = {}

        def add(msg: str, location: str) -> None:
            if msg:
                found.setdefault(msg, []).append(location)

        for directory in PY_DIRS:
            for path in sorted((base / directory).rglob("*.py")):
                for msg, line in self._from_python(path):
                    add(msg, f"{path.relative_to(base).as_posix()}:{line}")

        for path in sorted((base / TEMPLATE_DIR).rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(base).as_posix()
            for match in TRANS_TAG.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                add(match.group("msg"), f"{rel}:{line}")
            for match in BLOCK_TAG.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                add(match.group("msg").strip(), f"{rel}:{line}")

        return found

    def _from_python(self, path: Path):
        """Appels _( "..." ) / gettext( "..." ) a argument litteral."""
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names = {"_", "gettext", "gettext_lazy", "ngettext"}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            func = node.func
            label = getattr(func, "id", None) or getattr(func, "attr", None)
            if label not in names:
                continue
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                yield first.value, node.lineno

    # -- synchronisation ----------------------------------------------------

    def sync(self, base: Path, code: str, entries: dict[str, list[str]], *, check: bool) -> int:
        po_path = base / "locale" / code / "LC_MESSAGES" / "django.po"
        po_path.parent.mkdir(parents=True, exist_ok=True)

        if po_path.exists():
            catalog = polib.pofile(str(po_path), wrapwidth=0)
        else:
            catalog = polib.POFile(wrapwidth=0)
            catalog.metadata = {
                "Project-Id-Version": "konformix-site",
                "MIME-Version": "1.0",
                "Content-Type": "text/plain; charset=UTF-8",
                "Content-Transfer-Encoding": "8bit",
                "Language": code,
            }
        catalog.metadata["POT-Creation-Date"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M+0000"
        )

        known = {entry.msgid: entry for entry in catalog}
        for msgid, locations in entries.items():
            entry = known.get(msgid)
            if entry is None:
                entry = polib.POEntry(msgid=msgid, msgstr="")
                catalog.append(entry)
            entry.occurrences = [tuple(loc.rsplit(":", 1)) for loc in locations]
            entry.obsolete = False

        for entry in catalog:
            if entry.msgid not in entries:
                entry.obsolete = True

        missing = [e for e in catalog if not e.obsolete and not e.msgstr]

        if check:
            for entry in missing:
                self.stdout.write(self.style.WARNING(f"  [{code}] sans traduction : {entry.msgid[:70]}"))
            return len(missing)

        catalog.save(str(po_path))
        catalog.save_as_mofile(str(po_path.with_suffix(".mo")))
        translated = sum(1 for e in catalog if not e.obsolete and e.msgstr)
        total = sum(1 for e in catalog if not e.obsolete)
        self.stdout.write(
            self.style.SUCCESS(f"  {code} : {translated}/{total} traduites -> {po_path.parent}")
        )
        return len(missing)

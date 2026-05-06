from __future__ import annotations
from datetime import date

CZ_DAYS = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]

WASTE_DATA: dict[str, dict] = {
    "papir": {
        "label": "Papír",
        "icon": "mdi:newspaper-variant-outline",
        "emoji": "📄",
        "popis": (
            "🔵 Modrý pytel\n"
            "✅ Noviny, časopisy, katalogy, kartony, krabice, kancelářský papír, knihy, sešity, obalový papír, reklamní letáky, neznečištěné papírové sáčky\n"
            "❌ Kopírák, voskovaný papír, hygienické potřeby, papír znečištěný jídlem, plenky, textil, sklo, plasty, nebezpečný odpad"
        ),
        "dates": [
            date(2026, 1, 13),
            date(2026, 2, 10),
            date(2026, 3, 2),
            date(2026, 4, 7),
            date(2026, 5, 5),
            date(2026, 6, 16),
            date(2026, 7, 14),
            date(2026, 8, 11),
            date(2026, 9, 8),
            date(2026, 10, 6),
            date(2026, 11, 3),
            date(2026, 12, 7),
        ],
    },
    "plasty": {
        "label": "Plasty",
        "icon": "mdi:recycle",
        "emoji": "♻️",
        "popis": (
            "🟡 Žlutý pytel — plasty, tetrapack i kovy dohromady\n"
            "♻️ Plasty: PET lahve, fólie, mikrotenové sáčky, igelitové tašky, kelímky (jogurt, máslo, sýr), HDPE obaly (kečup, šampon, čisticí prostředky), polystyren, plastové hračky\n"
            "🧃 Tetrapack: kartony od mléka, džusů, vína\n"
            "🥫 Kovy: konzervy, plechovky od nápojů, sprejové nádobky, kovová víčka, obaly od čajových svíček"
        ),
        "dates": [
            date(2026, 1, 21),
            date(2026, 2, 18),
            date(2026, 3, 26),
            date(2026, 4, 30),
            date(2026, 5, 28),
            date(2026, 6, 25),
            date(2026, 7, 30),
            date(2026, 8, 27),
            date(2026, 9, 24),
            date(2026, 10, 29),
            date(2026, 11, 26),
            date(2026, 12, 21),
        ],
    },
    "komunal": {
        "label": "Komunální",
        "icon": "mdi:trash-can-outline",
        "emoji": "🗑️",
        "popis": (
            "⚫ Černá popelnice — svoz každý sudý týden v pondělí\n"
            "✅ Zbytky jídla, znečištěné obaly, hygienické potřeby, studený popel, keramika, porcelán\n"
            "❌ Tříděný odpad (plasty, papír, sklo, bio), nebezpečný odpad, elektro, léky, baterie, velkoobjemový odpad"
        ),
        "dates": [
            date(2026, 1, 5),
            date(2026, 1, 19),
            date(2026, 2, 2),
            date(2026, 2, 16),
            date(2026, 3, 2),
            date(2026, 3, 16),
            date(2026, 3, 30),
            date(2026, 4, 13),
            date(2026, 4, 27),
            date(2026, 5, 11),
            date(2026, 5, 25),
            date(2026, 6, 8),
            date(2026, 6, 22),
            date(2026, 7, 6),
            date(2026, 7, 20),
            date(2026, 8, 3),
            date(2026, 8, 17),
            date(2026, 8, 31),
            date(2026, 9, 14),
            date(2026, 9, 28),
            date(2026, 10, 12),
            date(2026, 10, 26),
            date(2026, 11, 9),
            date(2026, 11, 23),
            date(2026, 12, 7),
            date(2026, 12, 21),
        ],
    },
    "mobilni": {
        "label": "Mobilní sběrna",
        "icon": "mdi:truck",
        "emoji": "🚛",
        "popis": (
            "🚛 Přistavení od 6:00 do 20:00\n"
            "✅ Nábytek, matrace, koberce, spotřebiče, elektro, barvy, ředidla, kyseliny, oleje, léky, baterie, pneumatiky\n"
            "❌ Komunální odpad, tříděný odpad, stavební suť"
        ),
        "dates": [
            date(2026, 3, 14),
            date(2026, 9, 5),
        ],
    },
    "bioodpad": {
        "label": "Bioodpad",
        "icon": "mdi:leaf",
        "emoji": "🌿",
        "popis": (
            "🟤 Hnědá popelnice — svoz každý lichý týden v pátek, 6:00–20:00\n"
            "✅ Tráva, listí, zelenina, slupky z ovoce, kávový odpad, čajové sáčky, piliny, hobliny, větve (max. 25 cm, průřez 2 cm)\n"
            "❌ Hlína, potraviny, sklo, plasty, papír, kovy, léky, kosti, popel, podestýlka zvířat, hřbitovní odpad, elektroodpad\n"
            "⚠️ Pytle u popelnice nebudou sbírány! Pokuta za zakázaný obsah min. 1 000 Kč."
        ),
        "dates": [
            date(2026, 1, 16),
            date(2026, 2, 13),
            date(2026, 2, 27),
            date(2026, 3, 13),
            date(2026, 3, 27),
            date(2026, 4, 10),
            date(2026, 4, 24),
            date(2026, 5, 8),
            date(2026, 5, 22),
            date(2026, 6, 5),
            date(2026, 6, 19),
            date(2026, 7, 3),
            date(2026, 7, 17),
            date(2026, 7, 31),
            date(2026, 8, 14),
            date(2026, 8, 28),
            date(2026, 9, 11),
            date(2026, 9, 25),
            date(2026, 10, 9),
            date(2026, 10, 23),
            date(2026, 11, 6),
            date(2026, 11, 20),
            date(2026, 12, 4),
        ],
    },
}


def dates_to_str(dates: list[date]) -> str:
    return "\n".join(d.isoformat() for d in dates)


def parse_dates(dates_str: str) -> list[date]:
    result = []
    for line in dates_str.splitlines():
        line = line.strip().strip(",")
        if not line:
            continue
        try:
            result.append(date.fromisoformat(line))
        except ValueError:
            pass
    return sorted(result)


def resolve_dates(key: str, entry_data: dict, entry_options: dict) -> list[date]:
    """Priorita: options (editované uživatelem) → data (z první instalace) → výchozí."""
    for src in (entry_options, entry_data):
        if key in src and src[key] and src[key].strip():
            return parse_dates(src[key])
    return WASTE_DATA[key]["dates"]


def parse_ics(content: str) -> dict[str, list[date]]:
    """Parsuje ICS obsah, vrátí {název_události: [datumy]}."""
    events: dict[str, list[date]] = {}
    current: dict[str, object] = {}

    # Rozbalíme přeložené řádky (ICS standard: řádek začínající mezerou = pokračování)
    lines: list[str] = []
    for raw in content.splitlines():
        if raw.startswith((" ", "\t")) and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)

    for line in lines:
        if line == "BEGIN:VEVENT":
            current = {}
        elif line.upper().startswith("SUMMARY:"):
            current["summary"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("DTSTART"):
            value = line.split(":")[-1].strip()[:8]
            try:
                current["date"] = date(int(value[:4]), int(value[4:6]), int(value[6:8]))
            except (ValueError, IndexError):
                pass
        elif line == "END:VEVENT":
            s = current.get("summary")
            d = current.get("date")
            if s and d:
                events.setdefault(s, []).append(d)

    return {k: sorted(v) for k, v in events.items()}


def _next_date(dates: list[date]) -> date | None:
    today = date.today()
    future = [d for d in dates if d >= today]
    return future[0] if future else None


def _format_odpocet(days: int) -> str:
    if days < 0:
        return "Proběhl"
    if days == 0:
        return "Dnes!"
    if days == 1:
        return "Zítra"
    if days in (2, 3, 4):
        return f"Za {days} dny"
    return f"Za {days} dní"


def _format_den_datum(d: date) -> str:
    return f"{CZ_DAYS[d.weekday()]} {d.day}. {d.month}."

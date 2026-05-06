from __future__ import annotations
from datetime import date
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .data import WASTE_DATA, CZ_DAYS, resolve_dates, _next_date, _format_odpocet, _format_den_datum


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    resolved = {key: resolve_dates(key, entry.data, entry.options) for key in WASTE_DATA}

    entities: list[SensorEntity] = []
    for key, data in WASTE_DATA.items():
        entities.append(WasteSensor(key, data, resolved[key]))
    entities.append(WasteOverviewSensor(resolved))
    async_add_entities(entities, update_before_add=True)

    entry.async_on_unload(entry.add_update_listener(_async_reload))


async def _async_reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


class WasteSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, key: str, data: dict, dates: list[date]) -> None:
        self._key = key
        self._data = data
        self._dates = dates
        self._attr_name = f"Svoz {data['label']}"
        self._attr_unique_id = f"svoz_odpadu_{key}"
        self._attr_icon = data["icon"]

    def update(self) -> None:
        nd = _next_date(self._dates)
        if nd is None:
            self._attr_native_value = "Žádný termín"
            self._attr_extra_state_attributes = {
                "days": 999,
                "den_datum": "–",
                "datum": None,
                "label": self._data["label"],
                "emoji": self._data["emoji"],
                "popis": self._data.get("popis", ""),
            }
            return

        today = date.today()
        days = (nd - today).days
        self._attr_native_value = _format_odpocet(days)
        self._attr_extra_state_attributes = {
            "days": days,
            "den_datum": _format_den_datum(nd),
            "datum": nd.isoformat(),
            "label": self._data["label"],
            "emoji": self._data["emoji"],
            "popis": self._data.get("popis", ""),
        }


class WasteOverviewSensor(SensorEntity):
    _attr_name = "Svoz Prehled"
    _attr_unique_id = "svoz_odpadu_prehled"
    _attr_icon = "mdi:calendar-check-outline"
    _attr_should_poll = True
    _attr_native_unit_of_measurement = "dní"

    def __init__(self, resolved: dict[str, list[date]]) -> None:
        self._resolved = resolved

    def update(self) -> None:
        today = date.today()
        rows = []

        for key, data in WASTE_DATA.items():
            nd = _next_date(self._resolved.get(key, data["dates"]))
            if nd is None:
                continue
            days = (nd - today).days
            rows.append({
                "days": days,
                "emoji": data["emoji"],
                "label": data["label"],
                "den_datum": _format_den_datum(nd),
                "odpocet": _format_odpocet(days),
            })

        rows.sort(key=lambda r: r["days"])

        lines = []
        for r in rows:
            d = r["days"]
            badge = "🔴" if d <= 0 else "🟠" if d == 1 else "🟡" if d <= 3 else "🟢"
            lines.append(
                f"| {r['emoji']} | **{r['label']}** | {r['den_datum']} | {badge} {r['odpocet']} |"
            )

        table = (
            "| | Typ | Datum | Odpočet |\n"
            "|:---:|:---|:---|:---|\n"
            + "\n".join(lines)
        )

        self._attr_native_value = rows[0]["days"] if rows else 999
        self._attr_extra_state_attributes = {"tabulka": table}

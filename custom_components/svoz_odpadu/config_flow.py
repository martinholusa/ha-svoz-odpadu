from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    FileSelector,
    FileSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
)
from .const import DOMAIN
from .data import WASTE_DATA, dates_to_str, parse_ics

# Klíčová slova pro auto-detekci typu odpadu z názvu události v ICS
_KEYWORDS: dict[str, list[str]] = {
    "papir":    ["papír", "papir", "paper"],
    "plasty":   ["plast", "plastic", "pet"],
    "komunal":  ["komunál", "komunal", "směsný", "zbytkový", "zmesný", "mixed"],
    "bioodpad": ["bio", "biolog", "organick", "zelený", "green"],
}


def _auto_detect(waste_key: str, titles: list[str]) -> str:
    for title in titles:
        for kw in _KEYWORDS.get(waste_key, []):
            if kw in title.lower():
                return title
    return ""


def _mapping_schema(titles: list[str], defaults: dict[str, str]) -> vol.Schema:
    none_opt = {"value": "", "label": "— přeskočit —"}
    opts = [none_opt] + [{"value": t, "label": t} for t in titles]
    sel = SelectSelector(SelectSelectorConfig(options=opts, mode=SelectSelectorMode.DROPDOWN))
    return vol.Schema({
        vol.Required("map_papir",    default=defaults.get("papir",    "")): sel,
        vol.Required("map_plasty",   default=defaults.get("plasty",   "")): sel,
        vol.Required("map_komunal",  default=defaults.get("komunal",  "")): sel,
        vol.Required("map_bioodpad", default=defaults.get("bioodpad", "")): sel,
    })


def _build_dates_from_mapping(user_input: dict, parsed: dict[str, list]) -> dict[str, str]:
    result = {}
    for key in ("papir", "plasty", "komunal", "bioodpad"):
        mapped_title = user_input.get(f"map_{key}", "")
        if mapped_title and mapped_title in parsed:
            result[key] = dates_to_str(parsed[mapped_title])
    return result


# ---------------------------------------------------------------------------
# Společná logika kroků — sdílena mezi ConfigFlow a OptionsFlow
# ---------------------------------------------------------------------------

class _IcsMixin:
    """Mixin s kroky pro import ICS a mapování."""

    _parsed_ics: dict[str, list]  # {název_události: [date, ...]}

    async def _show_ics_file(self, user_input, errors=None):
        if user_input is not None:
            file_path = user_input.get("ics_file", "")
            try:
                def _read():
                    with open(file_path, encoding="utf-8") as f:
                        return f.read()
                content = await self.hass.async_add_executor_job(_read)
                self._parsed_ics = parse_ics(content)
                if not self._parsed_ics:
                    errors = {"base": "ics_empty"}
                else:
                    return await self.async_step_ics_mapping()
            except Exception:
                errors = {"base": "ics_parse_error"}
        return self.async_show_form(
            step_id="ics_file",
            data_schema=vol.Schema({
                vol.Required("ics_file"): FileSelector(
                    FileSelectorConfig(accept=".ics,text/calendar")
                )
            }),
            errors=errors or {},
        )

    async def _show_ics_url(self, user_input, errors=None):
        if user_input is not None:
            url = user_input["url"].strip()
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(url, timeout=15) as resp:
                    content = await resp.text()
                self._parsed_ics = parse_ics(content)
                if not self._parsed_ics:
                    errors = {"url": "ics_empty"}
                else:
                    return await self.async_step_ics_mapping()
            except Exception:
                errors = {"url": "cannot_connect"}
        return self.async_show_form(
            step_id="ics_url",
            data_schema=vol.Schema({vol.Required("url"): str}),
            errors=errors or {},
        )

    async def _show_ics_mapping(self, user_input):
        titles = list(self._parsed_ics.keys())
        defaults = {k: _auto_detect(k, titles) for k in ("papir", "plasty", "komunal", "bioodpad")}
        if user_input is not None:
            return _build_dates_from_mapping(user_input, self._parsed_ics)  # vrací dict
        return self.async_show_form(
            step_id="ics_mapping",
            data_schema=_mapping_schema(titles, defaults),
            description_placeholders={"count": str(len(titles)), "titles": ", ".join(titles[:5])},
        )


# ---------------------------------------------------------------------------
# Config Flow — první instalace
# ---------------------------------------------------------------------------

class SvozOdpaduConfigFlow(_IcsMixin, config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._parsed_ics: dict[str, list] = {}

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            method = user_input["method"]
            if method == "ics_file":
                return await self.async_step_ics_file()
            if method == "ics_url":
                return await self.async_step_ics_url()
            return self.async_create_entry(title="Svoz Odpadu", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("method", default="defaults"): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            {"value": "ics_file",  "label": "📂 Importovat ze souboru .ics"},
                            {"value": "ics_url",   "label": "🔗 Importovat z URL"},
                            {"value": "defaults",  "label": "✏️ Použít výchozí data (editovat později)"},
                        ],
                        mode=SelectSelectorMode.LIST,
                    )
                )
            }),
        )

    async def async_step_ics_file(self, user_input=None):
        return await self._show_ics_file(user_input)

    async def async_step_ics_url(self, user_input=None):
        return await self._show_ics_url(user_input)

    async def async_step_ics_mapping(self, user_input=None):
        result = await self._show_ics_mapping(user_input)
        if isinstance(result, dict):
            return self.async_create_entry(title="Svoz Odpadu", data=result)
        return result

    @staticmethod
    def async_get_options_flow(config_entry):
        return SvozOdpaduOptionsFlow(config_entry)


# ---------------------------------------------------------------------------
# Options Flow — editace přes ozubené kolečko
# ---------------------------------------------------------------------------

class SvozOdpaduOptionsFlow(_IcsMixin, config_entries.OptionsFlow):

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry
        self._parsed_ics: dict[str, list] = {}

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            method = user_input["method"]
            if method == "ics_file":
                return await self.async_step_ics_file()
            if method == "ics_url":
                return await self.async_step_ics_url()
            return await self.async_step_manual()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("method", default="manual"): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            {"value": "ics_file", "label": "📂 Importovat ze souboru .ics"},
                            {"value": "ics_url",  "label": "🔗 Importovat z URL"},
                            {"value": "manual",   "label": "✏️ Editovat termíny ručně"},
                        ],
                        mode=SelectSelectorMode.LIST,
                    )
                )
            }),
        )

    async def async_step_ics_file(self, user_input=None):
        return await self._show_ics_file(user_input)

    async def async_step_ics_url(self, user_input=None):
        return await self._show_ics_url(user_input)

    async def async_step_ics_mapping(self, user_input=None):
        result = await self._show_ics_mapping(user_input)
        if isinstance(result, dict):
            return self.async_create_entry(title="", data=result)
        return result

    async def async_step_manual(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        src = {**self._entry.data, **self._entry.options}
        defaults = {k: src.get(k, dates_to_str(WASTE_DATA[k]["dates"])) for k in WASTE_DATA}
        multiline = TextSelector(TextSelectorConfig(multiline=True))

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema({
                vol.Required("papir",    default=defaults["papir"]): multiline,
                vol.Required("plasty",   default=defaults["plasty"]): multiline,
                vol.Required("komunal",  default=defaults["komunal"]): multiline,
                vol.Required("bioodpad", default=defaults["bioodpad"]): multiline,
            }),
        )

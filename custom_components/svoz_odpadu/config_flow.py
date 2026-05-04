from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig
from .const import DOMAIN
from .data import WASTE_DATA, dates_to_str


class SvozOdpaduConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if user_input is not None:
            return self.async_create_entry(title="Svoz Odpadu", data={})
        return self.async_show_form(step_id="user")

    @staticmethod
    def async_get_options_flow(config_entry):
        return SvozOdpaduOptionsFlow(config_entry)


class SvozOdpaduOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        # Ukládáme jako _entry (soukromé) — vyhýbáme se konfliktu
        # s self.config_entry, které novější HA nastavuje automaticky
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        opts = self._entry.options
        defaults = {k: dates_to_str(v["dates"]) for k, v in WASTE_DATA.items()}
        multiline = TextSelector(TextSelectorConfig(multiline=True))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("papir",    default=opts.get("papir",    defaults["papir"])): multiline,
                vol.Required("plasty",   default=opts.get("plasty",   defaults["plasty"])): multiline,
                vol.Required("komunal",  default=opts.get("komunal",  defaults["komunal"])): multiline,
                vol.Required("bioodpad", default=opts.get("bioodpad", defaults["bioodpad"])): multiline,
            }),
        )

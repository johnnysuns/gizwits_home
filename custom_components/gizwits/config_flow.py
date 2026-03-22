from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import GizwitsApiClient, GizwitsApiError, GizwitsAuthError, GizwitsDevice
from .const import (
    CONF_APP_ID,
    CONF_DEVICE_NAME,
    CONF_DID,
    CONF_SCAN_INTERVAL,
    DEFAULT_GIZWITS_APP_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


class GizwitsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gizwits."""

    VERSION = 1

    def __init__(self) -> None:
        self._user_input: dict[str, Any] = {}
        self._devices: list[GizwitsDevice] = []

    @staticmethod
    def _map_error(err: GizwitsApiError) -> str:
        message = str(err).casefold()
        if "multiple devices matched" in message:
            return "multiple_devices"
        if "device not found" in message:
            return "device_not_found"
        return "cannot_connect"

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            manual_did = (user_input.get(CONF_DID) or "").strip()
            manual_name = (user_input.get(CONF_DEVICE_NAME) or "").strip()
            session = async_get_clientsession(self.hass)
            api = GizwitsApiClient(
                session,
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                user_input.get(CONF_APP_ID, DEFAULT_GIZWITS_APP_ID),
            )

            try:
                if manual_did:
                    await api.async_login()
                    await api.async_validate_did(manual_did)
                    self._user_input = {
                        **user_input,
                        CONF_DID: manual_did,
                        CONF_DEVICE_NAME: manual_name or manual_did,
                        "manual_did": True,
                    }
                    return await self._async_create_manual_entry()

                self._devices = await api.async_get_bindings()
            except GizwitsAuthError:
                _LOGGER.warning("Gizwits auth failed for user %s", user_input[CONF_USERNAME])
                errors["base"] = "invalid_auth"
            except GizwitsApiError as err:
                _LOGGER.exception("Gizwits config flow validation failed: %s", err)
                errors["base"] = self._map_error(err)
            else:
                self._user_input = user_input
                if not self._devices:
                    errors["base"] = "no_devices"
                elif len(self._devices) == 1:
                    return await self._async_create_entry_for_device(self._devices[0])
                else:
                    return await self.async_step_device()

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_APP_ID, default=DEFAULT_GIZWITS_APP_ID): str,
                vol.Optional(CONF_DID): str,
                vol.Optional(CONF_DEVICE_NAME): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                    int, vol.Range(min=15, max=3600)
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_device(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            did = user_input[CONF_DID]
            device = next((item for item in self._devices if item.did == did), None)
            if device is None:
                errors["base"] = "device_not_found"
            else:
                return await self._async_create_entry_for_device(device)

        options = {
            device.did: f"{device.name} ({device.did})"
            for device in self._devices
        }
        schema = vol.Schema(
            {
                vol.Required(CONF_DID): vol.In(options),
            }
        )
        return self.async_show_form(step_id="device", data_schema=schema, errors=errors)

    async def _async_create_entry_for_device(self, device: GizwitsDevice):
        data = {
            **self._user_input,
            CONF_DID: device.did,
            CONF_DEVICE_NAME: device.name,
            "manual_did": False,
        }
        await self.async_set_unique_id(f"{data[CONF_USERNAME]}::{device.did}")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=device.name, data=data)

    async def _async_create_manual_entry(self):
        did = self._user_input[CONF_DID]
        device_name = self._user_input.get(CONF_DEVICE_NAME) or did
        await self.async_set_unique_id(f"{self._user_input[CONF_USERNAME]}::{did}")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=device_name, data=self._user_input)

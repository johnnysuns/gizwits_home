from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GizwitsApiClient, GizwitsApiError
from .api import GizwitsDevice
from .const import CONF_DID, CONF_DEVICE_NAME, CONF_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class GizwitsDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Gizwits device data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: GizwitsApiClient,
        entry_data: dict[str, Any],
    ) -> None:
        interval = max(int(entry_data.get(CONF_SCAN_INTERVAL, 60)), MIN_SCAN_INTERVAL)
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )
        self.api = api
        self.entry_data = entry_data
        self.device = None

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            if self.device is None:
                did = self.entry_data.get(CONF_DID)
                device_name = self.entry_data.get(CONF_DEVICE_NAME)
                if did and self.entry_data.get("manual_did"):
                    self.device = GizwitsDevice(
                        did=did,
                        name=device_name or did,
                        product_name=None,
                        product_key=None,
                        is_online=None,
                    )
                else:
                    self.device = await self.api.async_resolve_device(
                        did,
                        device_name,
                    )
            latest = await self.api.async_get_latest(self.device.did)
        except GizwitsApiError as err:
            raise UpdateFailed(str(err)) from err

        attrs = latest.get("attr")
        if not isinstance(attrs, dict):
            attrs = {}
        normalized_attrs = {
            str(key).casefold(): value
            for key, value in attrs.items()
        }
        _LOGGER.debug(
            "Gizwits update ok for %s: %s",
            self.device.did,
            ", ".join(sorted(normalized_attrs.keys())),
        )

        return {
            "device": self.device,
            "updated_at": latest.get("updated_at"),
            "attrs": normalized_attrs,
            "raw_attrs": attrs,
        }

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import DEFAULT_GIZWITS_APP_ID, GIZWITS_API_BASE


class GizwitsApiError(Exception):
    """Base API error."""


class GizwitsAuthError(GizwitsApiError):
    """Authentication error."""


@dataclass(slots=True)
class GizwitsDevice:
    did: str
    name: str
    product_name: str | None
    product_key: str | None
    is_online: bool | None


class GizwitsApiClient:
    """Small Gizwits client."""

    def __init__(
        self,
        session: ClientSession,
        username: str,
        password: str,
        app_id: str = DEFAULT_GIZWITS_APP_ID,
    ) -> None:
        self._session = session
        self._username = username
        self._password = password
        self._app_id = app_id
        self._token: str | None = None

    @property
    def headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "X-Gizwits-Application-Id": self._app_id,
        }
        if self._token:
            headers["X-Gizwits-User-token"] = self._token
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        allow_401: bool = False,
    ) -> Any:
        try:
            async with self._session.request(
                method,
                f"{GIZWITS_API_BASE}{path}",
                headers=self.headers,
                json=json_body,
            ) as response:
                raw_text = await response.text()
                payload: Any = raw_text
                if raw_text:
                    try:
                        payload = json.loads(raw_text)
                    except json.JSONDecodeError:
                        payload = raw_text

                if response.status == 401 and not allow_401:
                    raise GizwitsAuthError("Unauthorized")
                if response.status >= 400:
                    raise GizwitsApiError(
                        f"HTTP {response.status}: {payload}"
                    )
                return payload
        except ClientError as err:
            raise GizwitsApiError(str(err)) from err

    async def async_login(self) -> str:
        payload = await self._request(
            "POST",
            "/app/login",
            json_body={
                "username": self._username,
                "password": self._password,
                "lang": "en",
            },
            allow_401=True,
        )
        token = payload.get("token") if isinstance(payload, dict) else None
        if not token:
            raise GizwitsAuthError("Login failed")
        self._token = token
        return token

    async def async_get_bindings(self) -> list[GizwitsDevice]:
        if not self._token:
            await self.async_login()

        devices: list[GizwitsDevice] = []
        skip = 0
        while True:
            payload = await self._request("GET", f"/app/bindings?limit=20&skip={skip}")
            page = payload.get("devices", []) if isinstance(payload, dict) else []
            for item in page:
                devices.append(
                    GizwitsDevice(
                        did=item["did"],
                        name=item.get("dev_alias") or item["did"],
                        product_name=item.get("product_name"),
                        product_key=item.get("product_key"),
                        is_online=item.get("is_online"),
                    )
                )
            if len(page) < 20:
                return devices
            skip += len(page)

    async def async_resolve_device(self, did: str | None, device_name: str | None) -> GizwitsDevice:
        devices = await self.async_get_bindings()
        if did:
            for device in devices:
                if device.did == did:
                    return device
            raise GizwitsApiError(f"Device not found for did: {did}")

        target = (device_name or "").strip().casefold()
        if not target:
            raise GizwitsApiError("Missing did or device name")

        exact = [device for device in devices if device.name.strip().casefold() == target]
        if len(exact) == 1:
            return exact[0]

        fuzzy = [device for device in devices if target in device.name.strip().casefold()]
        if len(fuzzy) == 1:
            return fuzzy[0]
        if len(fuzzy) > 1:
            names = ", ".join(f"{device.name} ({device.did})" for device in fuzzy)
            raise GizwitsApiError(f"Multiple devices matched: {names}")
        raise GizwitsApiError(f"Device not found: {device_name}")

    async def async_get_latest(self, did: str) -> dict[str, Any]:
        if not self._token:
            await self.async_login()
        try:
            payload = await self._request("GET", f"/app/devdata/{did}/latest")
        except GizwitsAuthError:
            await self.async_login()
            payload = await self._request("GET", f"/app/devdata/{did}/latest")

        if not isinstance(payload, dict):
            raise GizwitsApiError("Unexpected payload")
        return payload

    async def async_validate_did(self, did: str) -> dict[str, Any]:
        """Validate a device did by fetching the latest payload directly."""
        return await self.async_get_latest(did)

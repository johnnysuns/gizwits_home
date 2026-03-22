from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfFrequency, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GizwitsDataUpdateCoordinator

PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class GizwitsSensorDescription(SensorEntityDescription):
    key: str


SENSOR_DESCRIPTIONS: tuple[GizwitsSensorDescription, ...] = (
    GizwitsSensorDescription(
        key="p_value_p1",
        name="Phase 1 Active Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GizwitsSensorDescription(
        key="q_value_p1",
        name="Phase 1 Reactive Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GizwitsSensorDescription(
        key="i_value_p1",
        name="Phase 1 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GizwitsSensorDescription(
        key="u_value",
        name="Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GizwitsSensorDescription(
        key="f_value",
        name="Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GizwitsSensorDescription(
        key="e_value",
        name="Energy",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GizwitsSensorDescription(
        key="pf_value_p1",
        name="Phase 1 Power Factor",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GizwitsDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GizwitsSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    )


class GizwitsSensor(CoordinatorEntity[GizwitsDataUpdateCoordinator], SensorEntity):
    """Representation of a Gizwits metric."""

    entity_description: GizwitsSensorDescription

    def __init__(
        self,
        coordinator: GizwitsDataUpdateCoordinator,
        description: GizwitsSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True

    @property
    def available(self) -> bool:
        return self.entity_description.key.casefold() in self.coordinator.data.get("attrs", {})

    @property
    def unique_id(self) -> str:
        return f"{self.coordinator.device.did}_{self.entity_description.key}"

    @property
    def device_info(self) -> dict[str, object] | None:
        device = self.coordinator.data.get("device")
        if device is None:
            return None
        return {
            "identifiers": {(DOMAIN, device.did)},
            "name": device.name,
            "manufacturer": "Gizwits",
            "model": device.product_name or device.product_key or "Smart Meter",
        }

    @property
    def native_value(self) -> Decimal | str | None:
        raw = self.coordinator.data.get("attrs", {}).get(self.entity_description.key.casefold())
        if raw is None:
            return None
        try:
            return Decimal(str(raw))
        except (InvalidOperation, TypeError):
            return str(raw)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        attrs: dict[str, object] = {}
        if updated_at := self.coordinator.data.get("updated_at"):
            attrs["updated_at"] = updated_at
        return attrs

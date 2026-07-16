from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfReactivePower,
)
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
        translation_key="p_value_p1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    GizwitsSensorDescription(
        key="q_value_p1",
        translation_key="q_value_p1",
        native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    GizwitsSensorDescription(
        key="i_value_p1",
        translation_key="i_value_p1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    GizwitsSensorDescription(
        key="u_value",
        translation_key="u_value",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    GizwitsSensorDescription(
        key="f_value",
        translation_key="f_value",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    GizwitsSensorDescription(
        key="e_value",
        translation_key="e_value",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    GizwitsSensorDescription(
        key="pf_value_p1",
        translation_key="pf_value_p1",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=3,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GizwitsDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GizwitsSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class GizwitsSensor(CoordinatorEntity[GizwitsDataUpdateCoordinator], SensorEntity):
    """Representation of a Gizwits metric."""

    entity_description: GizwitsSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GizwitsDataUpdateCoordinator,
        description: GizwitsSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description

    @property
    def available(self) -> bool:
        return self.entity_description.key.casefold() in self.coordinator.data.get(
            "attrs", {}
        )

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
    def native_value(self) -> float | str | None:
        raw = self.coordinator.data.get("attrs", {}).get(
            self.entity_description.key.casefold()
        )
        if raw is None:
            return None
        try:
            return float(raw)
        except (TypeError, ValueError):
            return str(raw)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        attrs: dict[str, object] = {}
        if updated_at := self.coordinator.data.get("updated_at"):
            attrs["updated_at"] = updated_at
        return attrs

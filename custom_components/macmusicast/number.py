from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    client = hass.data[DOMAIN]["client"]
    async_add_entities([
        SystemVolumeNumber(client),
    ], True)

class SystemVolumeNumber(NumberEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "系统音量"
        self._attr_icon = "mdi:volume-high"
        self._attr_unique_id = "system_volume"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_mode = NumberMode.SLIDER
        self._attr_native_value = 50  # 默认音量
        self._attr_device_class = "volume"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            volume = await self.hass.async_add_executor_job(
                self._client.run_command,
                'osascript -e \'output volume of (get volume settings)\''
            )
            self._attr_native_value = int(volume.strip())
            self._attr_available = True
        except Exception as e:
            self._attr_available = False
            _LOGGER.error("Failed to get system volume: %s", e)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        try:
            await self.hass.async_add_executor_job(
                self._client.run_command,
                f'osascript -e \'set volume output volume {int(value)}\''
            )
            self._attr_native_value = value
            self._attr_available = True
        except Exception as e:
            self._attr_available = False
            _LOGGER.error("Failed to set system volume: %s", e) 
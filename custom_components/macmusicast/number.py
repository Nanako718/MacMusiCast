from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    client = hass.data[DOMAIN]["client"]
    async_add_entities([
        SystemVolumeNumber(client),
        MusicVolumeNumber(client),
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

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        volume = await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'output volume of (get volume settings)\''
        )
        try:
            self._attr_native_value = int(volume)
        except (ValueError, TypeError):
            self._attr_native_value = 50

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.hass.async_add_executor_job(
            self._client.run_command,
            f'osascript -e \'set volume output volume {int(value)}\''
        )
        self._attr_native_value = value

class MusicVolumeNumber(NumberEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Apple Music 音量"
        self._attr_icon = "mdi:music"
        self._attr_unique_id = "music_volume"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_mode = NumberMode.SLIDER
        self._attr_native_value = 50  # 默认音量

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        volume = await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to get sound volume\''
        )
        try:
            self._attr_native_value = int(volume)
        except (ValueError, TypeError):
            self._attr_native_value = 50

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.hass.async_add_executor_job(
            self._client.run_command,
            f'osascript -e \'tell application "Music" to set sound volume to {int(value)}\''
        )
        self._attr_native_value = value 
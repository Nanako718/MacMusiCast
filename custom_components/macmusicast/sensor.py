from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    client = hass.data[DOMAIN]["client"]
    async_add_entities([
        AppleMusicStateSensor(client),
        AppleMusicTrackSensor(client),
    ], True)

class AppleMusicStateSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._state = None
        self._attr_name = "Apple Music 播放状态"
        self._attr_icon = "mdi:music"
        self._attr_unique_id = "apple_music_state"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to get player state\''
        )

    @property
    def state(self):
        return self._state

class AppleMusicTrackSensor(SensorEntity):
    def __init__(self, client):
        self._client = client
        self._state = None
        self._attr_name = "Apple Music 当前曲目"
        self._attr_icon = "mdi:music-note"
        self._attr_unique_id = "apple_music_track"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to get name of current track\''
        )

    @property
    def state(self):
        return self._state 
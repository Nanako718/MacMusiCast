from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
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
        self._attr_available = False

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # 检查 Music 应用是否正在运行
            is_running = await self.hass.async_add_executor_job(
                self._client.run_command,
                'osascript -e \'application "Music" is running\''
            )
            
            if is_running.strip() == "true":
                self._state = await self.hass.async_add_executor_job(
                    self._client.run_command,
                    'osascript -e \'tell application "Music" to get player state\''
                )
                self._attr_available = True
            else:
                self._state = "stopped"
                self._attr_available = True
        except Exception as e:
            self._attr_available = False
            _LOGGER.error("Failed to get Apple Music state: %s", e)

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
        self._attr_available = False

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # 检查 Music 应用是否正在运行
            is_running = await self.hass.async_add_executor_job(
                self._client.run_command,
                'osascript -e \'application "Music" is running\''
            )
            
            if is_running.strip() == "true":
                self._state = await self.hass.async_add_executor_job(
                    self._client.run_command,
                    'osascript -e \'tell application "Music" to get name of current track\''
                )
                self._attr_available = True
            else:
                self._state = "未运行"
                self._attr_available = True
        except Exception as e:
            self._attr_available = False
            _LOGGER.error("Failed to get Apple Music track: %s", e)

    @property
    def state(self):
        return self._state 
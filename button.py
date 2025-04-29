from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    client = hass.data[DOMAIN]["client"]
    async_add_entities([
        AppleMusicPlayPauseButton(client),
        AppleMusicNextButton(client),
        AppleMusicPreviousButton(client),
    ], True)

class AppleMusicPlayPauseButton(ButtonEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Apple Music 播放/暂停"
        self._attr_icon = "mdi:play-pause"
        self._attr_unique_id = "apple_music_play_pause"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to playpause\''
        )

class AppleMusicNextButton(ButtonEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Apple Music 下一曲"
        self._attr_icon = "mdi:skip-next"
        self._attr_unique_id = "apple_music_next"

    async def async_press(self) -> None:
        """Handle the button press."""
        # 先切换到下一曲
        await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to next track\''
        )
        # 然后开始播放
        await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to play\''
        )

class AppleMusicPreviousButton(ButtonEntity):
    def __init__(self, client):
        self._client = client
        self._attr_name = "Apple Music 上一曲"
        self._attr_icon = "mdi:skip-previous"
        self._attr_unique_id = "apple_music_previous"

    async def async_press(self) -> None:
        """Handle the button press."""
        # 先切换到上一曲
        await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to previous track\''
        )
        # 然后开始播放
        await self.hass.async_add_executor_job(
            self._client.run_command,
            'osascript -e \'tell application "Music" to play\''
        ) 
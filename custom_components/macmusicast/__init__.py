import logging
import os
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .ssh_client import SSHClient
from .const import DOMAIN
from .sensor import AppleMusicStateSensor, AppleMusicTrackSensor
from .config_flow import MacMusicCastConfigFlow

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Mac Music Cast component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry):
    """Set up Mac Music Cast from a config entry."""
    conf = config_entry.data
    host = conf["host"]
    username = conf["username"]
    
    # 初始化域数据
    hass.data[DOMAIN] = {}
    
    # 根据认证方式获取相应的参数
    auth_type = conf.get("auth_type", "password")
    if auth_type == "password":
        client = SSHClient(host, username, password=conf.get("password"))
    else:
        client = SSHClient(host, username, private_key_file=conf.get("private_key_file"))

    hass.data[DOMAIN]["client"] = client

    # 加载品牌图标
    brand_image = os.path.join(os.path.dirname(__file__), "image.png")
    if os.path.isfile(brand_image):
        hass.data[DOMAIN]["brand_icon"] = brand_image

    # 注册实体
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "button")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "number")
    )

    async def play_pause(call):
        # 检查 Music 应用是否正在运行
        is_running = await hass.async_add_executor_job(
            client.run_command,
            'osascript -e \'application "Music" is running\''
        )
        
        if is_running.strip() == "true":
            # 如果正在运行，直接切换播放/暂停
            await hass.async_add_executor_job(
                client.run_command,
                'osascript -e \'tell application "Music" to playpause\''
            )
        else:
            # 如果未运行，先启动应用，然后等待一秒再开始播放
            await hass.async_add_executor_job(
                client.run_command,
                'osascript -e \'tell application "Music" to activate\''
            )
            await hass.async_add_executor_job(
                client.run_command,
                'sleep 1 && osascript -e \'tell application "Music" to play\''
            )

    async def next_track(call):
        await hass.async_add_executor_job(
            client.run_command,
            'osascript -e \'tell application "Music" to next track\''
        )

    async def previous_track(call):
        await hass.async_add_executor_job(
            client.run_command,
            'osascript -e \'tell application "Music" to previous track\''
        )

    hass.services.async_register(DOMAIN, "play_pause", play_pause)
    hass.services.async_register(DOMAIN, "next_track", next_track)
    hass.services.async_register(DOMAIN, "previous_track", previous_track)

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    hass.services.async_remove(DOMAIN, "play_pause")
    hass.services.async_remove(DOMAIN, "next_track")
    hass.services.async_remove(DOMAIN, "previous_track")
    
    # 卸载实体
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    await hass.config_entries.async_forward_entry_unload(entry, "number")
    
    return True

async def async_migrate_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        new = {**config_entry.data}
        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True 
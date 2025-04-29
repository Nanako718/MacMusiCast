from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN
from .ssh_client import SSHClient
import os

BRAND_IMAGE = "image.png"

async def async_setup_entry(hass, entry):
    """Set up from a config entry."""
    # 加载品牌图标
    brand_path = os.path.join(os.path.dirname(__file__), BRAND_IMAGE)
    if os.path.isfile(brand_path):
        hass.data[DOMAIN]["brand_icon"] = brand_path

class MacMusicCastConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                # 测试 SSH 连接
                client = SSHClient(
                    user_input["host"],
                    user_input["username"],
                    password=user_input.get("password"),
                    private_key_file=user_input.get("private_key_file")
                )
                # 测试连接
                test_result = await self.hass.async_add_executor_job(
                    client.run_command,
                    "echo 'SSH connection test'"
                )
                if test_result == "SSH connection test":
                    return self.async_create_entry(
                        title=f"Mac Music Cast - {user_input['host']}",
                        data=user_input
                    )
                else:
                    errors["base"] = "connection_failed"
            except Exception as e:
                errors["base"] = "connection_failed"

        schema_dict = {
            vol.Required("host"): str,
            vol.Required("username"): str,
        }

        # 添加认证方式选择
        auth_type = user_input.get("auth_type", "password") if user_input else "password"
        schema_dict[vol.Required("auth_type", default=auth_type)] = vol.In(
            ["password", "private_key"],
            "Authentication Type"
        )

        # 根据认证方式添加相应的字段
        if not user_input or user_input.get("auth_type") == "password":
            schema_dict[vol.Required("password")] = str
        else:
            schema_dict[vol.Required("private_key_file")] = str

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(schema_dict),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MacMusicCastOptionsFlow(config_entry)

class MacMusicCastOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema_dict = {
            vol.Required(
                "host",
                default=self._config_entry.data.get("host", "")
            ): str,
            vol.Required(
                "username",
                default=self._config_entry.data.get("username", "")
            ): str,
        }

        # 添加认证方式选择
        auth_type = self._config_entry.data.get("auth_type", "password")
        schema_dict[vol.Required("auth_type", default=auth_type)] = vol.In(
            ["password", "private_key"],
            "Authentication Type"
        )

        # 根据认证方式添加相应的字段
        if auth_type == "password":
            schema_dict[vol.Required(
                "password",
                default=self._config_entry.data.get("password", "")
            )] = str
        else:
            schema_dict[vol.Required(
                "private_key_file",
                default=self._config_entry.data.get("private_key_file", "")
            )] = str

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
        ) 
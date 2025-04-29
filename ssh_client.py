import paramiko
import logging

_LOGGER = logging.getLogger(__name__)

class SSHClient:
    def __init__(self, host, username, password=None, private_key_file=None):
        self._host = host
        self._username = username
        self._password = password
        self._private_key_file = private_key_file
        self._client = None

    def connect(self):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 根据提供的认证方式选择连接方法
            if self._password:
                self._client.connect(
                    self._host,
                    username=self._username,
                    password=self._password
                )
            elif self._private_key_file:
                self._client.connect(
                    self._host,
                    username=self._username,
                    key_filename=self._private_key_file
                )
            else:
                raise ValueError("Neither password nor private key file provided")

    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None

    def run_command(self, command):
        try:
            self.connect()
            stdin, stdout, stderr = self._client.exec_command(command)
            return stdout.read().decode().strip()
        except Exception as e:
            _LOGGER.error(f"Error executing command: {e}")
            return None 
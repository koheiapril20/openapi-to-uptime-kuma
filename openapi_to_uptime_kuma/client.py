from dotenv import load_dotenv
from uptime_kuma_api import UptimeKumaApi, MonitorType
import os
from typing import Dict, List
from .model import OperationMethod, MonitorEntry

load_dotenv()

def get_env_variable(name):
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Required environment variable '{name}' is not set.")
    return value


UPTIME_KUMA_API_URL = get_env_variable("UPTIME_KUMA_API_URL")
UPTIME_KUMA_USERNAME = get_env_variable("UPTIME_KUMA_USERNAME")
UPTIME_KUMA_PASSWORD = get_env_variable("UPTIME_KUMA_PASSWORD")

def upsert_monitors(dashboard: str, entries: List[MonitorEntry]):
    api = UptimeKumaApi(UPTIME_KUMA_API_URL)
    api.login(UPTIME_KUMA_USERNAME, UPTIME_KUMA_PASSWORD)

    monitor_dict: Dict[str, Dict] = {}
    monitors = api.get_monitors()
    for monitor in monitors:
        monitor_dict[monitor['name']] = monitor

    for entry in entries:
        for key, url in entry.get_urls().items():
            name = f'{dashboard}-{key}'

            if name in monitor_dict:
                pass
            else:
                api.add_monitor(
                    type=MonitorType.HTTP,
                    name=name,
                    url=url,
                    method=entry.method.value,
                )
    
    api.disconnect()

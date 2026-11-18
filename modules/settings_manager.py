from modules.core import get_default_save_path
import os
from modules.consts import SettingsParametrs
import json


BASE_SETTINGS = {
    SettingsParametrs.LANGUAGE.value: "en",
    SettingsParametrs.THEME.value: "maroon",
    SettingsParametrs.BASE_SAVE_PATH.value: get_default_save_path(),
    SettingsParametrs.DOWNLOADS_LIMIT.value: 3,
    SettingsParametrs.UPLOAD_SPEED_LIMIT.value: -1,
    SettingsParametrs.DOWNLOAD_SPEED_LIMIT.value: -1
}


class SettingManager:
    def __init__(self, settings_path: str):
        if not (os.path.exists(settings_path) or os.path.isfile(settings_path)):
            json.dump(BASE_SETTINGS, open(settings_path, "w"))

        self._settings_path: str = settings_path

    def get_settings(self) -> dict:
        try:
            with open(self._settings_path, "r") as file:
                settings = json.load(file)
                if (not settings or not isinstance(settings, dict) or
                    any(key not in settings.keys() for key in BASE_SETTINGS.keys())):
                    raise ValueError

                return settings

        except Exception:
            with open(self._settings_path, "w") as file:
                print("Settings error")
                file.write(json.dumps(BASE_SETTINGS))

            return self.get_settings()

    def set_default_setting(self, settings:dict, key: str) -> dict:
        with open(self._settings_path, "w") as file:
            settings[key] = BASE_SETTINGS[key]
            json.dump(settings, file)

        return settings

    def set_settings(self, new_settings: dict):
        with open(self._settings_path, "w") as file:
            json.dump(new_settings, file)

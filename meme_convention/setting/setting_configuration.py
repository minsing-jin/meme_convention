from pydantic import BaseModel, Field
from typing import Dict, List
import yaml
from pathlib import Path


class SystemSettingsModel(BaseModel):
    """Configuration for system settings."""
    music_enabled: bool = Field(default=False, description="Enable or disable music playback")
    keyboard_recording: bool = Field(default=False, description="Enable or disable keyboard typing recording")
    user_info: Dict[str, str] = Field(
        default_factory=lambda: {
            'Age': '',
            'Interest': '',
            'Country': '',
            'Location': '',
            'Job': ''
        },
        description="User information settings"
    )
    meme_contexts: List[str] = Field(default_factory=list, description="List of meme contexts")
    hot_key: str = Field(default="<ctrl>+<shift>+a", description="System settings hotkey")


class SystemSettingsConfiguration:
    def __init__(self, config_file_path: str = "system_settings.yaml"):
        self.config_file_path = Path(config_file_path)
        self.settings = self._load_settings()

    def _load_settings(self) -> SystemSettingsModel:
        """Load settings from YAML file or create default if file doesn't exist."""
        if self.config_file_path.exists():
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file) or {}
                return SystemSettingsModel(**data)
            except (yaml.YAMLError, Exception) as e:
                print(f"Error loading config file: {e}")
                return SystemSettingsModel()
        else:
            # Create default settings file
            default_settings = SystemSettingsModel()
            self._save_settings(default_settings)
            return default_settings

    def _save_settings(self, settings: SystemSettingsModel):
        """Save settings to YAML file."""
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(settings.model_dump(), file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Error saving config file: {e}")

    def get_settings(self) -> SystemSettingsModel:
        """Get current settings."""
        return self.settings

    def update_settings(self, **kwargs) -> bool:
        """Update specific settings and save to file."""
        try:
            # Update the settings with new values
            updated_data = self.settings.model_dump()
            updated_data.update(kwargs)

            # Validate the updated data
            new_settings = SystemSettingsModel(**updated_data)

            # Save to file
            self._save_settings(new_settings)
            self.settings = new_settings
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False

    def update_user_info(self, key: str, value: str) -> bool:
        """Update specific user info field."""
        user_info = self.settings.user_info.copy()
        user_info[key] = value
        return self.update_settings(user_info=user_info)

    def add_meme_context(self, context: str) -> bool:
        """Add a new meme context."""
        meme_contexts = self.settings.meme_contexts.copy()
        if context not in meme_contexts:
            meme_contexts.append(context)
            return self.update_settings(meme_contexts=meme_contexts)
        return True

    def remove_meme_context(self, context: str) -> bool:
        """Remove a meme context."""
        meme_contexts = self.settings.meme_contexts.copy()
        if context in meme_contexts:
            meme_contexts.remove(context)
            return self.update_settings(meme_contexts=meme_contexts)
        return True

    def reload_settings(self):
        """Reload settings from file."""
        self.settings = self._load_settings()


# 사용 예시
if __name__ == "__main__":
    # 설정 관리자 초기화
    config = SystemSettingsConfiguration("my_app_settings.yaml")

    # 현재 설정 조회
    current_settings = config.get_settings()
    print("Current settings:", current_settings.model_dump())

    # 설정 업데이트
    config.update_settings(music_enabled=True, keyboard_recording=True)

    # 사용자 정보 업데이트
    config.update_user_info("Age", "25")
    config.update_user_info("Country", "South Korea")

    # 밈 컨텍스트 추가
    config.add_meme_context("programming")
    config.add_meme_context("gaming")

    # 핫키 변경
    # TODO: hotkey setting change when user set
    config.update_settings(hot_key="<ctrl>+<shift>+s")

    print("Updated settings:", config.get_settings().model_dump())

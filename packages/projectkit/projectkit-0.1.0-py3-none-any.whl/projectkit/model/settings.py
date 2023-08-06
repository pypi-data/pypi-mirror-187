import json
from functools import reduce
from typing import Any, Callable, ClassVar, Hashable, Iterable, Literal, Optional, Union

import tomlkit
import yaml
from pydantic import BaseModel, DirectoryPath, FilePath

from projectkit.model.project import BaseProjectKitModelCLS
from projectkit.utils.map import (
    update_dictionary,
    get_definable_settings,
    update_defined_values,
    extended_schema,
    extended_group_schema,
)

DISALLOWED_KEYS_IN_SETTINGS_MSG = "{} collides with a built-in settings key in projectkit; refactoring is required"
SUPPORTED_FORMAT_TYPING = Literal["toml", "yaml"]
SETTINGS_TYPING = Union[str, dict[str, Any]]


class ProjectKitSettings(BaseModel):
    project_name: str = ...

    # Defined by choices during the initialization of the project instance, editing this portion should be with caution
    immutable_state_to_default: Optional[dict[str, Any]]
    # Settings defined by the meta project developer
    manual_settings_to_default: Optional[dict[str, SETTINGS_TYPING]]

    # The fields in these classes will be included as part of the settings, class derived settings (CDS)
    cds_single_classes_to_derive_settings: Optional[set[BaseProjectKitModelCLS]]
    cds_class_groups_to_derive_settings: Optional[dict[str, set[BaseProjectKitModelCLS]]]
    cds_include_field_types: bool = True

    setting_file_stem_suffix: str = "_settings"

    # Format related settings, use set_settings_format
    _settings_load: Callable = tomlkit.load
    _settings_dump: Callable = tomlkit.dump
    _settings_format: SUPPORTED_FORMAT_TYPING = "toml"

    # To avoid collisions with projectkit native settings fields
    _disallowed_keys_in_root_setting_dict: set[Hashable] = set("immutable")

    @classmethod
    def set_settings_format(cls, new_format: SUPPORTED_FORMAT_TYPING) -> None:
        if cls._settings_format == new_format:
            return

        match new_format:
            case "toml":
                cls._settings_load = tomlkit.load
                cls._settings_dump = tomlkit.dump
            case "yaml":
                cls._settings_load = yaml.safe_load
                cls._settings_dump = yaml.dump

    @classmethod
    @property
    def settings_file_stem(cls) -> str:
        return f"{cls.project_name}{cls.setting_file_stem_suffix}"

    @classmethod
    @property
    def settings_file_name(cls) -> str:
        return f"{cls.settings_file_stem}.{cls.settings_format}"

    @property
    def settings_format(self) -> str:
        return self._settings_format

    def settings_file_path(self, project_directory: DirectoryPath) -> FilePath:
        """

        :param project_directory: The path to the project directory related to the settings
        :return:
        """
        return project_directory / self.settings_file_name

    def dump_settings(self, settings: dict, project_directory: DirectoryPath) -> None:
        with open(self.settings_file_path(project_directory), "w") as out_settings:
            self._settings_dump(settings, out_settings)

    def load_settings(self, project_directory: DirectoryPath) -> SETTINGS_TYPING:
        with open(self.settings_file_path(project_directory), "r") as in_settings:
            return self._settings_load(in_settings)

    def new(self, silent: bool = True) -> dict[str, Union[str, dict[str, Any]]]:
        result = {}

        if self.immutable_state_to_default:
            result["immutable"] = self.immutable_state_to_default

        if self.manual_settings_to_default:
            self._settings_field_not_in_disallowed_keys(self.manual_settings_to_default.keys())
            result.update(self.manual_settings_to_default)

        if self.cds_single_classes_to_derive_settings:
            self._settings_field_not_in_disallowed_keys(
                (cls.__name__ for cls in self.cds_single_classes_to_derive_settings)
            )
            for cls in self.cds_single_classes_to_derive_settings:
                result.update(
                    extended_schema(
                        cls,
                        with_required=cls.projectkit_include_required,
                        with_optional=cls.projectkit_include_optional,
                    )
                )

        if self.cds_class_groups_to_derive_settings:
            for group_name, group in self.cds_class_groups_to_derive_settings.items():
                assert (
                    group_name not in self._disallowed_keys_in_root_setting_dict
                ), DISALLOWED_KEYS_IN_SETTINGS_MSG.format(group_name)
                result[group_name] = extended_group_schema(group)

        if not silent:
            print(json.dumps(result, indent=2))

        return result

    def dump_new(self, project_directory: DirectoryPath) -> None:
        self.dump_settings(self.new(silent=True), project_directory)

    def load_old(self, project_directory: DirectoryPath) -> SETTINGS_TYPING:
        return self.load_settings(project_directory)

    def update(
        self,
        project_directory: DirectoryPath,
        delete_outdated: bool = False,
        dry_run: bool = False,
        silent: bool = False,
    ) -> None:
        old_settings = self.load_old(project_directory)
        new_settings = self.new(silent=True)

        kwargs = {"delete_outdated": delete_outdated}

        for key in ("ingress", "definition_strategies", "perimeter"):
            if key in old_settings:
                try:
                    new_settings[key] = update_dictionary(old_settings[key], new_settings[key], **kwargs)
                except KeyError:
                    pass

        for key in ("manual_reader_kwargs", "experiment"):
            if key in old_settings:
                try:
                    new_settings[key] = update_defined_values(old_settings[key], new_settings[key], **kwargs)
                except KeyError:
                    pass

        if "trial" in old_settings:
            new_settings["trial"]["common"] = update_defined_values(
                old_settings["trial"]["common"], new_settings["trial"]["common"], **kwargs
            )
            common_settings_between_trials = get_definable_settings(new_settings["trial"]["common"])
            for trial_class_name, trial_class_settings in new_settings["trial"]["specific"].items():
                try:
                    new_settings["trial"]["specific"][trial_class_name] = update_defined_values(
                        old_settings["trial"]["specific"][trial_class_name],
                        trial_class_settings,
                        common_settings=common_settings_between_trials,
                        **kwargs,
                    )
                except KeyError:
                    pass

        for field, value in old_settings.items():
            if isinstance(value, dict):
                continue
            if field in new_settings and value:
                new_settings[field] = value

        if not dry_run:
            self.dump_settings(new_settings, project_directory)

        if not silent:
            print(json.dumps(new_settings, indent=2))

    def _settings_field_not_in_disallowed_keys(self, fields: Iterable[Hashable]) -> None:
        for field in fields:
            assert field not in self._disallowed_keys_in_root_setting_dict, DISALLOWED_KEYS_IN_SETTINGS_MSG.format(
                field
            )

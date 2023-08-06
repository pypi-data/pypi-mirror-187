from typing import ClassVar, Type

from pydantic import BaseModel


class BaseProjectKitModel(BaseModel):
    projectkit_include_required: ClassVar[bool] = True
    projectkit_include_optional: ClassVar[bool] = True

    @classmethod
    @property
    def projectkit_fields_to_exclude_from_settings_schema(cls) -> set[str]:
        """
        Some required fields for a class are sometimes highly specific to its respective object. These fields should
        be recorded in this class-property to be excluded by the settings generator function
        :return:
        """
        return set()

    @classmethod
    @property
    def projectkit_fields_to_force_include_from_settings_schema(cls) -> set[str]:
        """
        Some required fields for a class are sometimes highly specific to its respective object. These fields should
        be recorded in this class-property to be forcefully included by the settings generator function
        :return:
        """
        return set()


BaseProjectKitModelCLS = Type[BaseProjectKitModel]

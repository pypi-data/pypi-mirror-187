from functools import reduce
from typing import Iterable, Optional

from projectkit.model.project import BaseProjectKitModelCLS


def extended_schema(
    self, model_class: BaseProjectKitModelCLS, with_optional: bool = True, with_required: bool = True
) -> dict:
    assert with_optional or with_required

    class_schema = model_class.schema()
    required = (
        self.field_name_to_metadata(class_schema["required"], class_schema, model_class)
        if "required" in class_schema
        else {}
    )
    optional = self.field_name_to_metadata(
        set(class_schema["properties"]).difference(required), class_schema, model_class
    )

    defined, result = [], {}
    if required and with_required:
        defined.extend(required)
        result["required"] = required
    if with_optional:
        result["optional"] = optional

    return {"defined": {field: "" for field in defined}, **result}


def extended_group_schema(self, model_classes: Iterable, *args, **kwargs) -> dict:
    schemas = {
        model_class.__name__: self.extended_schema(model_class, *args, **kwargs) for model_class in model_classes
    }
    schema_names = tuple(schemas)
    first = schemas[schema_names[0]]

    specific, common = {}, {}
    for component in first:
        # Reduce till we have keys present in every set
        common_keys = set(reduce(set.intersection, map(lambda x: set(x[component]), schemas.values())))
        # Common keys are present in every schema; we can just get the metadata, v, from the first
        common[component] = {k: v for k, v in first[component].items() if k in common_keys}

        for name, schema in schemas.items():
            if difference := set(schema[component]).difference(common_keys):
                if name not in specific:
                    specific[name] = {}
                specific[name][component] = {k: v for k, v in schema[component].items() if k in difference}
            else:
                specific[name] = {"defined": {}}

    return {"common": common, "specific": specific}


def field_name_to_metadata(fields: Iterable, class_schema: dict, model_class: BaseProjectKitModelCLS) -> dict:
    result = {}
    for name in sorted(fields):
        if name in model_class.fields_to_exclude_from_settings_schema:
            continue

        field_property = class_schema["properties"][name]
        if "type" in field_property:
            field_type = field_property["type"]
        elif "anyOf" in field_property:
            field_type = field_property["anyOf"]
        elif "allOf" in field_property:
            field_type = field_property["allOf"]
        else:
            field_type = None

        if "default" in field_property:
            result[name] = f"{field_type} -> {field_property['default']}"
        else:
            result[name] = str(field_type)

    return result


def update_dictionary(old: dict, new: dict, delete_outdated: bool = False) -> dict:
    outdated_fields = set(old).difference(new)
    if outdated_fields and not delete_outdated:
        new["outdated"] = {}

    for field, value in old.items():
        if value is None:
            value = ""
        if field in new:
            if isinstance(value, dict):
                if field == "defined":
                    update_defined_dictionary(value, new[field], new["optional"], delete_outdated)
                else:
                    update_dictionary(value, new[field], delete_outdated)
            else:
                new[field] = value
        elif not delete_outdated:
            new["outdated"][field] = value

    return new


def update_defined_dictionary(old: dict, new: dict, new_optional: dict, delete_outdated: bool = False) -> dict:
    new_required_fields = set(old).difference(new)
    outdated_fields = new_required_fields.difference(new_optional)
    if outdated_fields and not delete_outdated:
        new["outdated"] = {}

    for field, value in old.items():
        if field in new or field in new_optional:
            new[field] = value
        elif not delete_outdated:
            new["outdated"][field] = value

    return new


def update_defined_values(
    old_values: dict, new_values: dict, common_settings: Optional[set] = None, delete_outdated: bool = False
) -> dict:
    old_defined = old_values["defined"]

    old_defined_fields = set(old_defined)
    new_definable_fields = get_definable_settings(new_values)
    if common_settings:
        new_definable_fields.update(common_settings)

    fields_to_keep = old_defined_fields.intersection(new_definable_fields)

    for sub_field, sub_value in old_defined.items():
        if sub_field in fields_to_keep:
            new_values["defined"][sub_field] = sub_value
        elif not delete_outdated:
            if "outdated" not in new_values["defined"]:
                new_values["defined"]["outdated"] = {}
            new_values["defined"]["outdated"][sub_field] = sub_value

    return new_values


def get_definable_settings(root_dict: dict) -> set:
    definable_fields = set()
    if "optional" in root_dict:
        definable_fields.update(root_dict["optional"])
    if "required" in root_dict:
        definable_fields.update(root_dict["required"])
    return definable_fields

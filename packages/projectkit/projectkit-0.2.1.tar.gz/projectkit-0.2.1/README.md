# ProjectKit: File-based settings utility

Supporting both YAML and TOML, your projects will have a user-friendly settings file. Native support for `Pydantic.model` in addition to Python `class`.

## Usage
The following generates two new files; `project_kit_demo.toml` and `project_kit_demo.lock.toml`
```python
from projectkit.model.settings import ProjectKitSettings

my_settings = ProjectKitSettings(project_name="showing_off", manual_setting_to_default={"leader_age": 96})

wild_user_input = int(input("How many participants? "))
number_of_participants = {
    "participants": [{"name": "", "age": 0} for _ in range(wild_user_input)]
}
my_settings.dump_new(project_directory=".", additional_settings=number_of_participants)
```

### Output
1. The settings file, `project_kit_demo.toml`:
```toml
leader_age = 96

[participants]
name = "age"
```
2. The settings lock file, `project_kit_demo.lock.toml`:
```toml
Python_version = "3.10.9"

[ProjectKit]
format = "toml"
version = "0.1.0"

[Locked]
leader_age = 96

[Locked.participants]
name = "age" 
```

## Installation
```shell
pip install projectkit
```
For those that prefer poetry:
```shell
poetry add projectkit
```

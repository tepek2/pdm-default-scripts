from collections.abc import MutableMapping
from typing import Any

import platformdirs
import tomlkit
from pdm.core import Core
from pdm.project import Project
from pdm.signals import post_init
from tomlkit import TOMLDocument
from tomlkit.items import Table

DEFAULT_SCRIPTS_FILE = "default-scripts.toml"


def _get_scripts_for_creation() -> Table | None:
    default_scripts = platformdirs.user_config_path("pdm") / DEFAULT_SCRIPTS_FILE

    if not default_scripts.exists():
        return None

    with default_scripts.open("r", encoding="utf-8") as fp:
        scripts = tomlkit.load(fp).get("scripts")

    if scripts is None:
        return None

    assert isinstance(scripts, Table), "[scripts] must be a TOML table"

    return scripts


def _add_script_with_dotted_keys(scripts_table: Table, name: str, command: Any):
    if isinstance(command, MutableMapping):
        for key, value in command.items():
            dotted_key = tomlkit.key([name, str(key)])
            scripts_table.append(dotted_key, value)
        return
    scripts_table[name] = command


def _get_or_create_table(node: TOMLDocument | Table, key: str) -> Table:

    if node.get(key) is None:
        node[key] = tomlkit.table()

    table = node[key]
    assert isinstance(table, Table), f"[{key}] must be TOML table"

    return table


def on_post_init(project: Project, **args):
    scripts_to_add = _get_scripts_for_creation()

    if scripts_to_add is None:
        return

    tool_table = _get_or_create_table(project.pyproject.open_for_write(), "tool")
    pdm_table = _get_or_create_table(tool_table, "pdm")
    scripts_table = _get_or_create_table(pdm_table, "scripts")

    for name, command in scripts_to_add.items():
        if name not in scripts_table:
            _add_script_with_dotted_keys(scripts_table, str(name), command)
            project.core.ui.info(f"Added default script: {name}")

    project.pyproject.write(show_message=False)


def plugin(core: Core) -> None:
    post_init.connect(on_post_init)

import tomlkit
import tomlkit.items
from pdm import signals
from pdm.project.core import Project
from pdm.pytest import RunResult
from pytest import MonkeyPatch

from default_scripts import on_post_init

pytest_plugins = "pdm.pytest"


def test_post_init_signal(
    project_no_init: Project,
    pdm,
    monkeypatch: MonkeyPatch,
):
    def _table_data(str_data: str) -> tomlkit.items.Table:
        scripts = tomlkit.parse(str_data).get("scripts")
        assert isinstance(scripts, tomlkit.items.Table)
        return scripts

    mock_config_file_str = """
    [scripts]
    _.env = { PYTHONPATH = "${PDM_PROJECT_ROOT}" }
    format = "ruff format ."
    cov = { cmd = "pytest --cov", env = { PYTHONPATH = "src" } }


    [scripts.cov2]
    cmd = "pytest --cov"
    env = { PYTHONPATH = "src" }
    """

    expected_data = {
        "_": {"env": {"PYTHONPATH": "${PDM_PROJECT_ROOT}"}},
        "format": "ruff format .",
        "cov": {"cmd": "pytest --cov", "env": {"PYTHONPATH": "src"}},
        "cov2": {"cmd": "pytest --cov", "env": {"PYTHONPATH": "src"}},
    }

    monkeypatch.setattr(
        "default_scripts._get_scripts_for_creation",
        lambda: _table_data(mock_config_file_str),
    )

    with signals.post_init.connected_to(on_post_init):
        result: RunResult = pdm(["init", "-n"], obj=project_no_init)
    print(project_no_init.scripts)
    assert result.exit_code == 0
    assert project_no_init.scripts == expected_data

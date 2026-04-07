![Github Actions](https://github.com/tepek2/pdm-default-scripts/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pdm-default-scripts?logo=python&logoColor=%23cccccc)](https://pypi.org/project/pdm-default-scripts)

# pdm-default-scripts

`pdm-default-scripts` is a PDM plugin that adds your predefined scripts to new projects right after `pdm init`.

## Installation

Install the plugin into your PDM environment:

```bash
pdm self add pdm-default-scripts
```

## Configure default scripts

Create a `default-scripts.toml` file in your user PDM config directory.

- Linux: `~/.config/pdm/default-scripts.toml`
- macOS: `~/Library/Application Support/pdm/default-scripts.toml`
- Windows: `%APPDATA%\\pdm\\default-scripts.toml`

### Example

```toml
[scripts]
test = "pytest"
lint = "ruff check ."
format = "ruff format ."

[scripts.cov]
cmd = "pytest --cov"
env = { PYTHONPATH = "src" }
```

## Usage

1. Configure `default-scripts.toml` once.
2. Run `pdm init` in any new project.
3. The plugin adds missing entries into `[tool.pdm.scripts]` in `pyproject.toml`.

Existing scripts are not overwritten.

## How it behaves

- Runs on the `post_init` PDM signal.
- Reads `[scripts]` from your `default-scripts.toml`.
- Writes scripts into `[tool.pdm.scripts]` only when a script name is not already present.

import importlib
import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    home_dir = tmp_path / "home"
    home_dir = home_dir.resolve()
    home_dir.mkdir()

    monkeypatch.chdir(home_dir)
    monkeypatch.setenv("HOME", str(home_dir))

    return home_dir


@pytest.fixture
def tmp_project(tmp_home, monkeypatch):
    project_dir = tmp_home / "project"
    project_dir.mkdir()
    monkeypatch.syspath_prepend(project_dir)

    return project_dir


@pytest.fixture
def tmp_bench(tmp_home, monkeypatch):
    bench_dir = tmp_home / "bench"
    bench_dir.mkdir()
    monkeypatch.chdir(bench_dir)

    return bench_dir


@pytest.fixture
def script_dir():
    return Path(__file__).parent.resolve() / "scripts"


@pytest.fixture
def lib_name():
    return "example_lib"


@pytest.fixture
def lib_file(lib_name):
    return f"{lib_name}.py"


@pytest.fixture
def exp():
    return "example_exp"


@pytest.fixture
def exp_file(exp):
    return f"{exp}.py"


@pytest.fixture
def tmp_lib_name(tmp_project, script_dir, lib_file, lib_name):
    shutil.copyfile(script_dir / lib_file, tmp_project / lib_file)
    return lib_name


@pytest.fixture
def tmp_lib(tmp_lib_name):
    lib_module = importlib.reload(importlib.import_module(tmp_lib_name))
    return lib_module


@pytest.fixture
def tmp_lib_exp(tmp_project, script_dir, exp_file, exp):
    shutil.copyfile(script_dir / exp_file, tmp_project / exp_file)
    return exp


@pytest.fixture
def tmp_bench_exp(tmp_bench, script_dir):
    shutil.copyfile(script_dir / exp_file, tmp_bench / exp_file)


@pytest.fixture
def data_dir(tmp_path):
    dd = tmp_path / "data"
    dd.mkdir()
    return dd


@pytest.fixture
def data_root_env_var(data_dir, monkeypatch):
    monkeypatch.setenv("PROJECT_DATA_ROOT", str(data_dir))


@pytest.fixture
def tmp_lib_with_data_root_env_var(tmp_lib_name, data_root_env_var, monkeypatch):
    monkeypatch.setattr(os, "environ", os.environ.copy())
    lib_module = importlib.reload(importlib.import_module(tmp_lib_name))
    return lib_module


@pytest.fixture
def env_file_content(data_dir):
    return f"PROJECT_DATA_ROOT={str(data_dir)}\n"


@pytest.fixture
def tmp_project_env_file(tmp_project, env_file_content):
    env_file = tmp_project / ".env"
    env_file.touch()
    env_file.write_text(env_file_content)


@pytest.fixture
def tmp_lib_with_tmp_project_env_file(tmp_lib_name, tmp_project_env_file, monkeypatch):
    monkeypatch.setattr(os, "environ", os.environ.copy())
    lib_module = importlib.reload(importlib.import_module(tmp_lib_name))
    return lib_module

import os

import pytest

from root_dir.data_root import DataRoot


class TestDataRoot:
    def test_init(self, tmp_path):
        DataRoot(data_root=tmp_path)

    def test_init_create(self, tmp_path):
        DataRoot(data_root=tmp_path / "subdir1", create_if_needed=True)

        with pytest.raises(FileNotFoundError):
            DataRoot(data_root=tmp_path / "subdir2", create_if_needed=False)

    def test_init_create_parents(self, tmp_path):
        DataRoot(
            data_root=tmp_path / "dir1" / "subdir",
            create_if_needed=True,
            create_parents_if_needed=True,
        )

        with pytest.raises(FileNotFoundError):
            DataRoot(data_root=tmp_path / "dir2" / "subdir", create_if_needed=False)

        with pytest.raises(FileNotFoundError):
            DataRoot(
                data_root=tmp_path / "dir3" / "subdir",
                create_if_needed=True,
                create_parents_if_needed=False,
            )

    def test_from_env_var(
        self, tmp_project, tmp_lib_with_data_root_env_var, data_dir, monkeypatch
    ):
        monkeypatch.chdir(tmp_project)
        assert tmp_lib_with_data_root_env_var.dr.data_root == data_dir

    def test_standard_env_file_setup(
        self, tmp_project, data_dir, tmp_lib_with_tmp_project_env_file, monkeypatch
    ):
        monkeypatch.chdir(tmp_project)
        assert tmp_lib_with_tmp_project_env_file.dr.data_root == data_dir

    def test_env_file_from_bench(
        self, tmp_bench, data_dir, tmp_lib_with_tmp_project_env_file, monkeypatch
    ):
        assert tmp_lib_with_tmp_project_env_file.dr.data_root == data_dir

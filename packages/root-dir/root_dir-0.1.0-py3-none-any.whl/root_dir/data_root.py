import io
import os
from pathlib import Path
from typing import Union, Type, TypeVar

import dotenv
from environment_files import find_environment
from liblog import get_logger

import root_dir.data_dir as data_dir

logger = get_logger()

# Type hint help
DD = TypeVar("DD", bound=data_dir.DataDir)


class DataRoot:
    logger = get_logger(name_suffix=".DataRoot")

    def __init__(
        self,
        data_root: Union[str, Path],
        create_if_needed: bool = False,
        create_parents_if_needed: bool = False,
    ):
        self.logger.info("Using provided data_root:")
        self.logger.info(str(data_root))
        data_root = Path(data_root).absolute()
        try:
            assert data_root.exists()
        except AssertionError as e:
            if create_if_needed:
                self.logger.info("Creating data root directory:")
                self.logger.info(str(data_root))
                data_root.mkdir(exist_ok=True, parents=create_parents_if_needed)
            else:
                raise FileNotFoundError() from e
        self.data_root = data_root

    def __getattr__(self, item):
        return getattr(self.data_root, item)

    @classmethod
    def from_env_var(
        cls,
        env_var_name: str = "DATA_ROOT",
        env_var_prefix: str = None,
        capitalize_env_var: bool = True,
        override_env_var: bool = False,
        set_env_var: bool = True,
        explicit_env_file_path: Union[str, Path] = None,
        env_file_name: str = ".env",
        find_env_file_from_main: bool = False,
        find_env_file_from_cwd: bool = False,
        stack_height_above_caller: int = 0,
        stop_env_file_search_at: Union[str, Path] = "root",
        create_if_needed: bool = False,
        create_parents_if_needed: bool = False,
    ):
        env_var_name = cls.setup_env_var_name(
            env_var_name, env_var_prefix, capitalize_env_var
        )

        if not override_env_var:
            try:
                data_root = os.environ[env_var_name]
                return cls(
                    data_root,
                    create_if_needed=create_if_needed,
                    create_parents_if_needed=create_parents_if_needed,
                )
            except KeyError:
                pass

        if explicit_env_file_path is not None:
            explicit_env_file_path = Path(explicit_env_file_path).absolute()
            if explicit_env_file_path.is_file():
                env_file_name = explicit_env_file_path.name
                explicit_env_file_path = explicit_env_file_path.parent
            else:
                assert explicit_env_file_path.is_dir()

        try:
            env_file = find_environment(
                file_name=env_file_name,
                from_main=find_env_file_from_main,
                from_cwd=find_env_file_from_cwd,
                from_path=explicit_env_file_path,
                stop_at=stop_env_file_search_at,
                raise_error=False,
            )
        except ValueError:
            logger.error("default run mode: from_caller")
            env_file = find_environment(
                file_name=env_file_name,
                from_caller=True,
                stop_at=stop_env_file_search_at,
                stack_height_above_caller=stack_height_above_caller + 1,
            )

        env_values = dotenv.dotenv_values(env_file)
        data_root = env_values[env_var_name]

        if set_env_var:
            os.environ[env_var_name] = data_root

        return cls(
            data_root,
            create_if_needed=create_if_needed,
            create_parents_if_needed=create_parents_if_needed,
        )

    @classmethod
    def setup_env_file(
        cls,
        env_file_path: Union[str, Path],
        data_root: Union[str, Path],
        env_file_name: str = ".env",
        env_var_name: str = "DATA_ROOT",
        env_var_prefix: str = None,
        capitalize_env_var: bool = True,
    ):
        env_file_path = Path(env_file_path).absolute()
        if env_file_path.is_dir():
            env_file_path = env_file_path / env_file_name

        env_var_name = cls.setup_env_var_name(
            env_var_name, env_var_prefix, capitalize_env_var
        )

        data_root = Path(data_root)

        env_values = dotenv.dotenv_values(env_file_path)
        if env_var_name in env_values:
            assert (
                Path(env_values[env_var_name]).resolve() == data_root.resolve()
            ), f"Variable {env_var_name} is already set to a different value in env file {str(env_file_path)}"

            cls.logger.info(
                f"Variable {env_var_name} is already set in env file {str(env_file_path)}"
            )
        else:
            with open(env_file_path, "rb+") as env_file:
                env_file.seek(-1, io.SEEK_END)
                last_char = env_file.read(1)

                if len(last_char) == 0 or last_char == b"\n":
                    env_file.write(
                        f"{env_var_name}={str(data_root.absolute())}".encode()
                    )
                else:
                    env_file.write(
                        f"\n{env_var_name}={str(data_root.absolute())}".encode()
                    )

    @staticmethod
    def setup_env_var_name(env_var_name, env_var_prefix, capitalize_env_var):
        if env_var_prefix is not None:
            env_var_name = f"{env_var_prefix}_{env_var_name}"
        if capitalize_env_var:
            env_var_name = env_var_name.upper()
        return env_var_name

    def get_data_dir(
        self,
        relpath: Path,
        data_dir_cls: Type[DD] = data_dir.DataDir,
        **kwargs,
    ) -> DD:
        return data_dir_cls(data_relpath=relpath, data_root=self, **kwargs)

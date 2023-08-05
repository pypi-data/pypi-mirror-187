from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass
class DataDir:
    data_relpath: Union[str, Path]
    data_root: Path

    def __post_init__(self):
        self.data_relpath = Path(self.data_relpath)

    @property
    def data_dir(self):
        data_dir = self.data_root / self.data_relpath
        assert data_dir.exists()
        return data_dir

    def subdir(self, relpath: Union[Path, str]):
        return DataDir(
            data_root=self.data_root, data_relpath=self.data_relpath / relpath
        )

    def __getattr__(self, item):
        return getattr(self.data_dir, item)

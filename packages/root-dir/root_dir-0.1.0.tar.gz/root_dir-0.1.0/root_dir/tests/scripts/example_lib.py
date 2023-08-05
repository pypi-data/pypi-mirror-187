import logging

logging.basicConfig()

from root_dir.data_root import DataRoot
import root_dir

root_dir.unmute()

dr = DataRoot.from_env_var(
    env_var_prefix="PROJECT",
)

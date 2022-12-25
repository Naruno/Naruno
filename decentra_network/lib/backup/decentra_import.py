import os
import shutil
import sys
from typing import Union

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("LIB")


def decentra_import(export_location: str) -> None:
    """
    Extract a ZIP archive to the `db` folder in the main directory of the application.

    Args:
        export_location: The location of the ZIP archive to be extracted.
    """
    logger.info("Import system is started")
    main_folder = get_config()["main_folder"]
    target_location = f"{main_folder}/db/"
    logger.debug(f"export_location: {export_location}")
    logger.debug(f"target_location: {target_location}")
    shutil.unpack_archive(export_location, target_location)
    logger.info("Import completed")

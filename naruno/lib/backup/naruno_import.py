import copy
import os
import shutil
import sys
from typing import Union

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from naruno.lib.config_system import get_config, save_config
from naruno.lib.log import get_logger
from naruno.lib.settings_system import save_settings, temp_json, the_settings

logger = get_logger("LIB")


def naruno_import(export_location: str) -> None:
    """
    Extract a ZIP archive to the `db` folder in the main directory of the application.

    Args:
        export_location: The location of the ZIP archive to be extracted.
    """
    logger.info("Import system is started")
    backup_config = copy.copy(get_config())
    main_folder = backup_config["main_folder"]
    target_location = f"{main_folder}/db/"
    logger.debug(f"export_location: {export_location}")
    logger.debug(f"target_location: {target_location}")
    shutil.unpack_archive(export_location, target_location)

    save_config(backup_config)

    after_backup_settings = the_settings()
    for element in temp_json:
        if element not in after_backup_settings:
            after_backup_settings[element] = temp_json[element]

    save_settings(after_backup_settings)

    logger.info("Import completed")

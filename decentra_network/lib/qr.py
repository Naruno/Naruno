#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

from decentra_network.config import QR_CODE_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from hashlib import sha256


logger = get_logger("LIB")


def qr(data):
    logger.info("Qr code generator is started")
    logger.debug(f"data: {data}")
    main_folder = get_config()["main_folder"]
    data_sha256 = sha256(data.encode("utf-8")).hexdigest()
    location = f"{main_folder}/{QR_CODE_PATH}{data_sha256}.png"
    logger.info(f"location: {location}")

    if not os.path.exists(location):
        logger.info("Qr code is not exist, it will be created")
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)
        icon = f"{main_folder}/gui_lib/images/logo_w_bc.png"
        logger.debug(icon)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            embeded_image_path=icon,
            color_mask=SolidFillColorMask(front_color=(94, 194, 149)),
        )
        qr_img.save(location)
    else:
        logger.info("Qr code already exists")

    logger.info("Qr code generator is finished.")
    return location

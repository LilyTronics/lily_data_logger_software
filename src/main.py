"""
Start up script for the application
"""

import os
import wx

from src.app_data import AppData
from src.controllers.controller_main import ControllerMain
from src.models.logger import Logger


if not os.path.isdir(AppData.USER_FOLDER):
    os.makedirs(AppData.USER_FOLDER)

logger = Logger()
logger.info("Start application")
logger.debug(f"Application path     : {AppData.APP_PATH}")
logger.debug(f"User instruments path: {AppData.USER_FOLDER}")
app = wx.App(redirect=False)
ControllerMain(f"{AppData.APP_NAME} V{AppData.VERSION}", logger)
app.MainLoop()
logger.info("Application stopped")
logger.shut_down()

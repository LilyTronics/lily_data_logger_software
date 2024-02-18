"""
View for logger.
"""

import wx

from src.models.id_manager import IdManager
from src.models.image_data import ImageData
from src.models.logger import Logger


class ViewLogger(wx.Frame):

    _UPDATE_TIME = 300
    _WINDOW_MIN_SIZE = (800, 500)

    _COLOR_DEFAULT = "#000"

    _TEXT_COLORS = {
        Logger.TYPE_DEBUG: "#666",
        Logger.TYPE_ERROR: "#f60",
        Logger.TYPE_INFO: "#00f",
        Logger.TYPE_STDERR: "#f00",
        Logger.TYPE_STDOUT: "#999"
    }

    def __init__(self, title):
        self._filename = Logger.get_filename()
        super().__init__(None, wx.ID_ANY, title)
        self.SetIcon(wx.Icon(ImageData.show_log.Bitmap))

        self._txt_console = wx.TextCtrl(self, IdManager.ID_LOG_MESSAGES,
                                        style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY |
                                              wx.TE_RICH)
        self._txt_console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_NORMAL, False))

        self._update_timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self._on_update_timer, self._update_timer)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.SetInitialSize(self._WINDOW_MIN_SIZE)

    def _on_update_timer(self, event):
        with open(self._filename, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        content = self._txt_console.GetValue()
        for line in filter(lambda x: x not in content, lines):
            for key, value in self._TEXT_COLORS.items():
                if f" | {key:6} | " in line:
                    self._txt_console.SetDefaultStyle(wx.TextAttr(value))
                    break
            else:
                self._txt_console.SetDefaultStyle(wx.TextAttr(self._COLOR_DEFAULT))

            self._txt_console.AppendText(line)

        event.Skip()

    def _on_close(self, event):
        self._update_timer.Stop()
        self._update_timer.Destroy()
        event.Skip()

    def show(self):
        self._update_timer.Start(self._UPDATE_TIME)
        self.Show()


if __name__ == "__main__":

    import pylint
    import random
    import threading
    import time


    def _generate_exception():
        _ = 1 / 0

    def _generate_messages(logger):
        logger_types = [
            logger.debug,
            logger.error,
            logger.info,
            print
        ]

        log_nr = 0
        while True:
            log_type = random.randint(0, len(logger_types))
            if log_type < len(logger_types):
                logger_types[log_type](f"Log message number {log_nr}")
            else:
                et = threading.Thread(target=_generate_exception)
                et.start()
            time.sleep(random.uniform(0.3, 0.6))
            log_nr += 1

    log = Logger()
    log.info("Start thread for generating messages")

    mt = threading.Thread(target=_generate_messages, args=(log, ))
    mt.daemon = True
    mt.start()

    app = wx.App(redirect=False)
    frame = ViewLogger("Test log messages")
    frame.show()
    app.MainLoop()

    log.shut_down()
    pylint.run_pylint([__file__])

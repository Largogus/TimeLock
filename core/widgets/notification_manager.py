from loguru import logger
from Widgets.Notification import Notification
from core.command.notificatoion_commands import on_focus_rollup


class NotificationManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.queue = []
        self.is_showing = False

    def show(self, text, name=None, hwnd=None):
        logger.debug(self.queue)
        if self.queue and self.queue[-1][1] == name:
            return

        self.queue.append((text, name, hwnd))

        if not self.is_showing:
            self._show_next()

    def _show_next(self):
        if not self.queue:
            self.is_showing = False
            return

        self.is_showing = True

        text, name, hwnd = self.queue.pop(0)

        if hwnd is not None:
            on_focus_rollup()

        self.notification = Notification(text, parent=self.parent)

        self.notification.show_notification(name, hwnd)

        self.notification.closed.connect(self._show_next)
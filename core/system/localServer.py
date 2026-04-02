from PySide6.QtNetwork import QLocalServer, QLocalSocket
from loguru import logger
from core.system.focus_system import bring_to_front

SERVER_NAME = "TimeLockSingletonServer"
local_server = None


def send_raise_signal():
    socket = QLocalSocket()
    socket.connectToServer(SERVER_NAME)

    if not socket.waitForConnected(1000):
        return False

    socket.write(b'raise')
    socket.flush()
    socket.waitForBytesWritten(1000)
    socket.disconnectFromServer()
    return True


def start_local_server(window):
    global local_server

    local_server = QLocalServer()

    QLocalServer.removeServer(SERVER_NAME)

    if not local_server.listen(SERVER_NAME):
        logger.error("Не удалось запустить локальный сервер")
        return

    def handle_connection():
        sock = local_server.nextPendingConnection()

        def read_data():
            data = sock.readAll().data()
            if data == b'raise':
                logger.info("Получена команда raise, поднимаем окно")

                bring_to_front(window)

        sock.readyRead.connect(read_data)

    local_server.newConnection.connect(handle_connection)

    logger.success("LocalServer запущен")
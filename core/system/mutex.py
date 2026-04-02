import ctypes
from ctypes import wintypes
from loguru import logger

ERROR_ALREADY_EXISTS = 183
CREATE_MUTEX_INITIAL_OWNER = 0x00000001


kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

CreateMutexW = kernel32.CreateMutexW
CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
CreateMutexW.restype = wintypes.HANDLE

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL


class SingleInstance:
    def __init__(self, mutex_name="Global\\TimeLock_App_Mutex_2026"):
        self.mutex_name = mutex_name
        self.mutex = None
        self.is_first_instance = False

    def acquire(self):
        self.mutex = CreateMutexW(
            None,
            False,
            self.mutex_name
        )

        if self.mutex is None:
            logger.error("Не удалось создать мьютекс")
            return False

        last_error = ctypes.get_last_error()

        if last_error == ERROR_ALREADY_EXISTS:
            logger.info("Другой экземпляр TimeLock уже запущен. Активируем его окно...")
            self.release()
            return False

        self.is_first_instance = True
        logger.success("Мьютекс захвачен — это первый экземпляр приложения")
        return True

    def release(self):
        if self.mutex:
            CloseHandle(self.mutex)
            self.mutex = None


single_instance = SingleInstance()
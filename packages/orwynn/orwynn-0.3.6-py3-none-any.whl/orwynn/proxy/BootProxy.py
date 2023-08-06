from pathlib import Path
from typing import TYPE_CHECKING

from orwynn.apprc.AppRC import AppRC
from orwynn.boot.BootMode import BootMode
from orwynn.worker.Worker import Worker

if TYPE_CHECKING:
    from orwynn.app.ErrorHandler import ErrorHandler
    from orwynn.indication.Indication import Indication


class BootProxy(Worker):
    """Proxy data to prevent DI importing Boot worker directly (and avoid
    circular imports by this) to build BootConfig.
    """
    def __init__(
        self,
        *,
        root_dir: Path,
        mode: BootMode,
        api_indication: "Indication",
        apprc: AppRC,
        ErrorHandlers: list[type["ErrorHandler"]]
    ) -> None:
        super().__init__()
        self.__root_dir: Path = root_dir
        self.__mode: BootMode = mode
        self.__api_indication: Indication = api_indication
        self.__apprc: AppRC = apprc
        self.__ErrorHandlers: list[type["ErrorHandler"]] = ErrorHandlers

    @property
    def mode(self) -> BootMode:
        return self.__mode

    @property
    def api_indication(self) -> "Indication":
        return self.__api_indication

    @property
    def apprc(self) -> AppRC:
        return self.__apprc

    @property
    def ErrorHandlers(self) -> list[type["ErrorHandler"]]:
        return self.__ErrorHandlers

    @property
    def boot_config_data(self) -> dict:
        return {
            "root_dir": self.__root_dir,
            "mode": self.__mode,
            "api_indication": self.__api_indication,
            "app_rc": self.__apprc,
            "ErrorHandlers": self.__ErrorHandlers
        }

    @property
    def data(self) -> dict:
        return dict(**self.boot_config_data, **{})

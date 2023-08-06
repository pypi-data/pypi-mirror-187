from pathlib import Path

from pytest import fixture

from orwynn.boot.BootMode import BootMode
from orwynn.indication.default_api_indication import default_api_indication
from orwynn.proxy.BootProxy import BootProxy


@fixture
def std_boot_data_proxy() -> BootProxy:
    return BootProxy(
        root_dir=Path.cwd(),
        mode=BootMode.TEST,
        api_indication=default_api_indication,
        apprc={},
        ErrorHandlers=[]
    )

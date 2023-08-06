from orwynn.app.App import App
from orwynn.app.ErrorHandler import ErrorHandler
from orwynn.controller.Controller import Controller
from orwynn.di.collecting.collect_modules import collect_modules
from orwynn.di.collecting.collect_provider_dependencies import (
    collect_provider_dependencies,
)
from orwynn.di.DIContainer import DIContainer
from orwynn.di.DIObject import DIObject
from orwynn.di.init.init_other_acceptors import init_other_acceptors
from orwynn.di.init.init_providers import init_providers
from orwynn.middleware.Middleware import Middleware
from orwynn.module.Module import Module
from orwynn.validation import validate
from orwynn.worker.Worker import Worker


class DI(Worker):
    """Resolves Dependency-injection related tasks for an application.

    Only objects in categories Providers and Acceptors take part in DI. For now
    only objects from BUILTIN_PROVIDERS and BUILTIN_ACCEPTORS are considered.
    In future it might be possible to add custom providers or acceptors (maybe
    using class decorators) in addition to builtin ones.

    Stages of DI:
    - Build a dependency tree, collecting all objects and their requested
        injections
    - Make an order of initialization for dependencies
    - Initialize dependencies according to the order for each making
        appropriate injections

    How high in order dependency will be placed depends on:
    - Dependency's priority, see BUILTIN_PROVIDERS
    - Amount of other dependencies and their priorities:
    ```
    dep1 * dep1_priority + dep2 * dep2_priority + ... + dep_n * dep_n_priority
    ```
    - Amount of imports of other modules at the module, where considered
        dependency resides

    Attributes:
        root_module:
            Root module of the app.
    """
    def __init__(self, root_module: Module) -> None:
        super().__init__()
        validate(root_module, Module)

        # So here we have generally two stages of DI:
        #   1. Collecting (module "di/collecting")
        #   2. Initializing (module "di/init")

        self.modules: list[Module] = collect_modules(root_module)
        self.__container: DIContainer = init_providers(
            collect_provider_dependencies(self.modules)
        )
        init_other_acceptors(self.__container, self.modules)

    @property
    def app_service(self) -> App:
        app = self.find("App")
        if isinstance(app, App):
            return app
        else:
            raise TypeError(
                f"{app} is not an App instance"
            )

    @property
    def controllers(self) -> list[Controller]:
        """Fetches all controllers from container.

        Returns:
            All controllers fetched.
        """
        return self.__container.controllers

    @property
    def all_middleware(self) -> list[Middleware]:
        """Fetches all middleware from container.

        Returns:
            All middleware fetched.
        """
        return self.__container.all_middleware

    @property
    def error_handlers(self) -> list[ErrorHandler]:
        return self.__container.error_handlers

    def find(self, key: str) -> DIObject:
        """Returns DI object by its key.

        Note that searching is made using PascalCased keys, but actual object
        returned is an initialized instance of searched class.

        Args:
            key:
                String value to search with.

        Returns:
            A DIObject found.

        Raises:
            MissingDIObjectError:
                DIObject with given key is not found.
        """
        return self.__container.find(key)

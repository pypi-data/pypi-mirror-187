"""List of classes an user can subclass from."""
from orwynn.BaseSubclassable import BaseSubclassable
from orwynn.controller.Controller import Controller
from orwynn.error.Error import Error
from orwynn.middleware.Middleware import Middleware
from orwynn.model.Model import Model
from orwynn.service.Service import Service

# Note that here listed the most basic classes. E.g. Config and ErrorHandler
# are not listed since they are derivatives from model and on the stage of DI
# it will be checked to find these more specific classes.
SUBCLASSABLES: list[BaseSubclassable] = [
    Service,
    Controller,
    Middleware,
    Model,
    Error
]

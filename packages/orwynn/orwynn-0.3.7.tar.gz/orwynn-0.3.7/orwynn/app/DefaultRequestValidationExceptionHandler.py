from orwynn.app.ErrorHandler import ErrorHandler
from orwynn.proxy.BootProxy import BootProxy
from orwynn.validation import RequestValidationException
from orwynn.web import JSONResponse, Request, Response


class DefaultRequestValidationExceptionHandler(ErrorHandler):
    E = RequestValidationException

    def handle(
        self,
        request: Request,
        error: RequestValidationException
    ) -> Response:
        return JSONResponse(
            BootProxy.ie().api_indication.digest(error),
            422
        )

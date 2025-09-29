# Python modules
from typing import Any

# Django modules
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def hello_view(
    request: HttpRequest,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any]
) -> HttpResponse:
    """
    Return a simple HTML page.

    Parameters:
        request: HttpRequest
            The request object.
        *args: list
            Additional positional arguments.
        **kwargs: dict
            Additional keyword arguments.
    
    Returns:
        HttpResponse
            Rendered HTML page with a name in the context.
    """

    return render(
        request=request,
        template_name="index.html",
        context={"name": "Dias", "names": []},
        status=200
    )

def users_info(
        request: HttpRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
) -> HttpResponse:
    
    return render(
        request=request,
        template_name="users.html",
        context={"users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]},
    )
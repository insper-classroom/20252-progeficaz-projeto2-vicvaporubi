"""
Simple HATEOAS utilities for the Imoveis API
"""

from flask import url_for


def add_links_to_imovel(imovel):
    """Add simple HATEOAS links to a single imovel"""
    if not isinstance(imovel, dict) or "id" not in imovel:
        return imovel

    imovel_copy = dict(imovel)
    imovel_copy["_links"] = {
        "self": {
            "href": url_for("get_imovel", id=imovel["id"], _external=True),
            "method": "GET",
        },
        "edit": {
            "href": url_for("update_imovel", id=imovel["id"], _external=True),
            "method": "PUT",
        },
        "delete": {
            "href": url_for("delete_imovel", id=imovel["id"], _external=True),
            "method": "DELETE",
        },
        "all": {"href": url_for("get_all_imoveis", _external=True), "method": "GET"},
        "tipo": {
            "href": url_for("get_imoveis_by_tipo", tipo=imovel["tipo"], _external=True),
            "method": "GET",
        },
        "cidade": {
            "href": url_for(
                "get_imoveis_by_cidade", cidade=imovel["cidade"], _external=True
            ),
            "method": "GET",
        },
    }
    return imovel_copy


def add_links_to_collection(imoveis):
    """Add simple HATEOAS links to a collection of imoveis"""
    if not imoveis:
        return []

    return [add_links_to_imovel(dict(imovel)) for imovel in imoveis]


def create_success_response(message, id=None):
    """Create a success response with navigation links"""
    response = {"message": message}
    response["_links"] = {
        "all": {"href": url_for("get_all_imoveis", _external=True), "method": "GET"},
        "create": {"href": url_for("create_imovel", _external=True), "method": "POST"},
    }
    if id:
        response["_links"]["created"] = {
            "href": url_for("get_imovel", id=id, _external=True),
            "method": "GET",
        }
    return response


def create_error_response(message):
    """Create an error response with navigation links"""
    return {
        "error": message,
        "_links": {
            "all": {
                "href": url_for("get_all_imoveis", _external=True),
                "method": "GET",
            },
            "home": {"href": url_for("home", _external=True), "method": "GET"},
        },
    }

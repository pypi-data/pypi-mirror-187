#!/usr/bin/python
#
# Copyright 2018-2023 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

from django.http import HttpRequest

from polyaxon.services.headers import PolyaxonServiceHeaders

try:
    from rest_framework import HTTP_HEADER_ENCODING
except ImportError:
    raise ImportError("This module depends on django rest.")


POLYAXON_HEADERS_USER_ID = "X_POLYAXON_USER_ID"
POLYAXON_HEADERS_PUBLIC_ONLY = "X_POLYAXON_PUBLIC_ONLY"


def get_header(request: HttpRequest, header_service: str):
    """Return request's 'X_POLYAXON_...:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    service = request.META.get("HTTP_{}".format(header_service), b"")
    if isinstance(service, str):
        # Work around django test client oddness
        service = service.encode(HTTP_HEADER_ENCODING)
    return service


def get_service_header(request: HttpRequest):
    """Return request's 'X_POLYAXON_SERVICE:' header, as a bytestring."""
    return get_header(request=request, header_service=PolyaxonServiceHeaders.SERVICE)


def get_internal_header(request: HttpRequest) -> str:
    """
    Return request's 'X_POLYAXON_INTERNAL:' header, as a bytestring.
    """
    return get_header(request=request, header_service=PolyaxonServiceHeaders.INTERNAL)

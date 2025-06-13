from django.http import HttpRequest


def absolute_media_url_builder(request: HttpRequest, media_url: str):
    return request.build_absolute_uri(media_url)

import http.client
import ssl
import urllib

from django.conf import settings


def send_pushover(message):
    context = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.pushover.net:443",context=context)
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": settings.PUSHOVER_TOKEN,
                "user": settings.PUSHOVER_USER_KEY,
                "message": message,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()

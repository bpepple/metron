import http.client
import json
import logging
import ssl
import urllib.parse

from django.conf import settings

from metron.settings import RAPID_API_HOST, RAPID_API_KEY

LOGGER = logging.getLogger(__name__)


def check_email_domain(email: str):
    try:
        conn = http.client.HTTPSConnection("mailcheck.p.rapidapi.com")

        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_API_HOST,
        }

        conn.request("GET", f"/?domain={email}", headers=headers)

        res = conn.getresponse()
        match res.status:
            case 200:
                data = res.read()
                result = json.loads(data.decode("utf-8"))
            case _:
                LOGGER.warning(f"Bad response from RapidAPI: {res.status} {res.reason}")
                result = None
    except http.client.HTTPException as e:
        LOGGER.error(f"HTTP error: {e}")
        result = None
    except Exception as e:  # NOQA: BLE001
        LOGGER.error(f"An error occurred: {e}")
        result = None
    finally:
        conn.close()

    return result


def send_pushover(message):
    context = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.pushover.net:443", context=context)
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

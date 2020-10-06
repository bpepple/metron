import json
import urllib

from metron import settings


def get_recaptcha_auth(request):
    recaptcha_response = request.POST.get("g-recaptcha-response")
    url = "https://www.google.com/recaptcha/api/siteverify"
    values = {
        "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response,
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)

    return json.loads(response.read().decode())

import json
import urllib.parse
import urllib.request

from metron import settings


def get_recaptcha_auth(request):
    hcaptcha_response = request.POST.get("h-captcha-response")
    url = "https://hcaptcha.com/siteverify"
    values = {
        "secret": settings.HCAPTCHA_SECRET_KEY,
        "response": hcaptcha_response,
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)

    return json.loads(response.read().decode())

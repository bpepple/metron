from rest_framework import throttling


class PostUserRateThrottle(throttling.UserRateThrottle):
    scope = "post_user"

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class GetUserRateThrottle(throttling.UserRateThrottle):
    scope = "get_user"

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)

""" Python class to communicate with ShortBoxed """
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import platform


class ShortBoxedTalker:
    def __init__(self) -> None:
        self.api_base_url = "https://api.shortboxed.com"
        self.user_agent = f"sb-import/0.0.1 ({platform.system()}; {platform.release()})"

    def fetch_response(self, url: str):
        """ Function to retrieve a response from ShortBoxed """
        request = Request(url)
        request.add_header("User-Agent", self.user_agent)

        try:
            content = urlopen(request)
        except HTTPError as http_error:
            # TODO: Look into handling throttling better, but for now let's use this.
            if http_error.code == 429:
                print("Exceeded api rate limit. Sleeping for 30 seconds...")
                time.sleep(30)
                return self.fetch_response(url)
            print(f"HTTP error: {http_error.reason}")
        except URLError as url_error:
            print(f"Connection error: {url_error.reason}")
        else:
            return json.loads(content.read().decode("utf-8"))

    def fetch_query_request(self, release_date: str, publisher: str):
        """ release_date should be in iso8601 format (ie: 2016-02-17) """
        url = f"{self.api_base_url}/comics/v1/query?release_date={release_date}&publisher={publisher.lower()}"
        return self.fetch_response(url)

    def convert_json_to_list(self, results):
        return results["comics"]

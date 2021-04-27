""" Some utility function to cleanup data from Shortboxed """


def _remove_trade_paperbacks(lst):
    """ Remove any comic that doesn't have an issue number """
    return [i for i in lst if "#" in i["title"]]


def _cleanup_title(str):
    """ Remove any word *after* the issue number """
    words = str.split(" ")
    new_title = []
    for i in words:
        if i.startswith("#"):
            new_title.append(i.strip())
            return " ".join(new_title)
        new_title.append(i.strip())

    return " ".join(new_title)


def _remove_duplicate_titles(lst):
    """ Remove any duplicate issues from the Shortboxed data """
    seen = set()
    result = []
    for item in lst:
        if item["title"] not in seen:
            seen.add(item["title"])
            result.append(item)

    return result


def clean_shortboxed_data(lst):
    """ Clean up the title data from Shortboxed so we can query the db """
    for i in lst:
        i["title"] = _cleanup_title(i["title"])

    lst = _remove_trade_paperbacks(lst)
    lst = _remove_duplicate_titles(lst)

    return lst

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


def _print_series_choices(series_list):
    for (counter, series_name) in enumerate(series_list, start=1):
        print(f"{counter}. {series_name}")


def select_series_choice(series_list):
    _print_series_choices(series_list)

    while True:
        i = input("Choose a series #, or 's' to skip: ")
        if (i.isdigit() and int(i) in range(1, len(series_list) + 1)) or i == "s":
            break

    if i != "s":
        i = int(i) - 1
        return series_list[i]
    else:
        return None

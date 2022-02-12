""" Some utility function to cleanup data from Shortboxed """
import dateutil.relativedelta


def _remove_trade_paperbacks(lst):
    """Remove any comic that doesn't have an issue number"""
    return [i for i in lst if "#" in i.title]


def _cleanup_title(str):
    """Remove any word *after* the issue number"""
    words = str.split(" ")
    new_title = []
    for i in words:
        if i.startswith("#"):
            new_title.append(i.strip())
            return " ".join(new_title)
        new_title.append(i.strip())

    return " ".join(new_title)


def _remove_duplicate_titles(lst):
    """Remove any duplicate issues from the Shortboxed data"""
    seen = set()
    result = []
    for item in lst:
        if item.title not in seen:
            seen.add(item.title)
            result.append(item)

    return result


def clean_description(text):
    result = text.rstrip("Rated T+")
    result = result.rstrip("Rated T")
    result = result.rstrip("Parental Advisory")
    return result


def clean_shortboxed_data(lst):
    """Clean up the title data from Shortboxed so we can query the db"""
    for i in lst:
        i.title = _cleanup_title(i.title)

    lst = _remove_trade_paperbacks(lst)
    lst = _remove_duplicate_titles(lst)

    return lst


def _print_list_choices(results_list):
    for (counter, series_name) in enumerate(results_list, start=1):
        print(f"{counter}. {series_name}")


def _print_issue_choices(results_list):
    for (counter, issue) in enumerate(results_list, start=1):
        print(f"{counter}. {issue.title}")


def select_list_choice(results_list):
    if len(results_list) > 1:
        print("Multiple results found:")
    else:
        print("One record found:")

    _print_list_choices(results_list)

    while True:
        i = input("Choose a item #, or 's' to skip: ")
        if (i.isdigit() and int(i) in range(1, len(results_list) + 1)) or i == "s":
            break

    if i != "s":
        i = int(i) - 1
        return results_list[i]
    else:
        return None


def select_issue_choice(results):
    if len(results) > 1:
        print("Multiple results found:")
    else:
        print("One record found:")

    _print_issue_choices(results)

    while True:
        i = input("Choose a item #, or 's' to skip: ")
        if (i.isdigit() and int(i) in range(1, len(results) + 1)) or i == "s":
            break

    if i != "s":
        i = int(i) - 1
        return results[i]
    else:
        return None


def determine_cover_date(release_date, publisher):
    if publisher.upper() != "MARVEL COMICS":
        return release_date.replace(day=1)

    new_date = release_date + dateutil.relativedelta.relativedelta(months=2)
    return new_date.replace(day=1)


def get_query_values(item):
    name = item.title.split("#")
    return name[0].strip(), name[1]

import re

from urllib.request import urlopen

LEARN_TO_LEAD_URL = "https://urbanclimb.com.au/stuff-to-do/learn-the-ropes/"


def get_page_as_string() -> str:
    return urlopen(LEARN_TO_LEAD_URL).read().decode('utf-8')


def get_new_listings(
    gyms: list[str],
    old_listings: list[tuple[str, str, str]]
) -> list[tuple[str, str, str]]:
    """
    Returns the "Learn to Lead" course listings for the provided gyms which
    are not already included in the old listings.
    """

    gym_regex = f"({'|'.join(gyms)})"
    sep = "→"
    dates_regex = "([0-9ndsth, ]*)"
    months_regex = "(January|February|March|April|May|June|July|August|September|October|November|December)"

    regex = f"{gym_regex} {sep} {dates_regex} {months_regex}"

    current_listings = re.findall(regex, get_page_as_string(), flags = re.IGNORECASE)

    return [listing for listing in current_listings if listing not in old_listings]

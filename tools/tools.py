from langchain_community.utilities import SerpAPIWrapper


def get_profile_url(text: str) -> str:
    """Searches for a valid LinkedIn URL profile page."""
    search = SerpAPIWrapper()
    res = search.run(f"{text}")
    return res

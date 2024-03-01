from langchain_community.utilities import SerpAPIWrapper

def get_profile_url(text: str) -> str:
    """Searches for a person from their name and returns information from their various social media."""
    search = SerpAPIWrapper()
    res = search.run(f"{text}")
    return res



import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information frmo the LinkedIn profile"""
    choice = 2
    api_endpoint = "0"
    response = 0
    if choice == 1:
        api_endpoint = "https://api.github.com/gists/fc2ea284f71972d8c40d5528dd879f98"
        response = requests.get(api_endpoint)
    if choice == 2:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
        )

    linkedin_data = response.json()

    linkedin_data = {
        k: v
        for k, v in linkedin_data.items()
        if (v not in ([], "", "", None))
        and k not in ["people_also_viewed", "certifications"]
    }
    if linkedin_data.get("groups"):
        for group_dict in linkedin_data.get("groups"):
            group_dict.pop("profile_pic_url")

    return linkedin_data

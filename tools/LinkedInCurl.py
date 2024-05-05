import json
import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()

@tool
def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""


 
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url},
        headers=header_dic
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    json_dic = data
    return json_dic


# if "__main__":
#     result = scrape_linkedin_profile("https://www.linkedin.com/in/bryan-gomez-87708b179/")
#     print(result)



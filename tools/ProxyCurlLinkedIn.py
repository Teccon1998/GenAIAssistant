import os
import requests
from dotenv import load_dotenv
import json  # Import json for better handling of json data

load_dotenv()

def scrapelinkedinprofile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles, manually scrape the information from the LinkedIn profile."""

    if mock:
        # Use a mocked URL for testing
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        # Real API endpoint
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(api_endpoint, params={"url": "https://www.linkedin.com/in/chidansh/","skills":"include"}, headers=header_dic)

    # Convert response to JSON
    data = response.json()
    
    # Clean up data to remove empty values and specific keys
    clean_data = {k: v for k, v in data.items() if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]}
    
    # Handling nested dictionaries in 'groups', if present
    if clean_data.get("groups"):
        for group_dict in clean_data["groups"]:
            group_dict.pop("profile_pic_url", None)  # Use pop with None as default to avoid KeyError

    # Convert cleaned data back to JSON for output
    json_data = json.dumps(clean_data, indent=4)  # Convert dictionary to JSON string with pretty print

    print(json_data)

    return (clean_data)

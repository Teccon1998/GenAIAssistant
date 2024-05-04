import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
import json

load_dotenv()

@tool
def scrape_job(linkedin_job_url: str):
    """Scrape information from LinkedIn jobs,
    when a linkedIn job url is given, use this tool to return information about the job"""

    # Use the live API with authentication
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/job'
    headers = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    response = requests.get(api_endpoint, params={"url": linkedin_job_url}, headers=headers)

    data = response.json()

    # Define the keys that you are interested in keeping
    # relevant_keys = {'job_title', 'location', 'salary', 'skills', 'company_name', 'job_description'}

    # # Filter the data to include only the relevant job-specific fields
    # filtered_data = {
    #     key: value
    #     for key, value in data.items()
    #     if key in relevant_keys and value not in ([], "", None)
    # }

    # Remove unwanted keys from groups if present
    if "groups" in data:
        for group_dict in data["groups"]:
            group_dict.pop("profile_pic_url", None)  # Use pop with None to avoid KeyError

    print(json.dumps(data, indent=4))  # Print filtered data in JSON format

    return data  # Return the filtered data for further use

# Example call
# scrape_job("https://linkedin.com/job/somejobid", mock=True)

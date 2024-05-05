import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
import json

load_dotenv()

@tool
def scrape_job(linkedin_job_url: str)->dict:
    """Scrape information from LinkedIn jobs,
    when a LinkedIn job url is given, use this tool to return information about the job"""

    # Use the live API with authentication
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/job'
    headers = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    response = requests.get(api_endpoint, params={"url": linkedin_job_url}, headers=headers)

    data = response.json()

    # Optional: Define the keys that you are interested in keeping
    relevant_keys = {'job_title', 'location', 'salary', 'skills', 'company_name', 'job_description'}

    # Filter the data to include only the relevant job-specific fields (uncomment if you want filtering)
    filtered_data = {
        key: value
        for key, value in data.items()
        if key in relevant_keys and value not in ([], "", None)
    }

    # Remove unwanted keys from groups if present
    if "groups" in filtered_data:
        for group_dict in filtered_data["groups"]:
            group_dict.pop("profile_pic_url", None)

    # Convert the filtered data to a JSON string
    json_data = json.dumps(filtered_data, indent=4)  # Convert dictionary to JSON formatted string
    print(json_data)  # Print the JSON formatted string
    return filtered_data  # Return the JSON formatted string

# Example call
# scrape_job("https://linkedin.com/job/somejobid")

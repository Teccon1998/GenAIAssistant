import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

@tool
def scrape_linkedin_job(linkedin_job_url: str):
    """scrape information from LinkedIn jobs,
    Manually scrape the information from the LinkedIn jobs for information, when data is found stop the execution """


    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/job'
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    response = requests.get(
        api_endpoint,
        params={"url": linkedin_job_url},
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

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_job(
            linkedin_job_url="https://www.linkedin.com/in/eden-marco/",
        )
    )
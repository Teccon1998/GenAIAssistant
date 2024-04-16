import os
from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
from dotenv import load_dotenv

load_dotenv()

open_api_key = os.environ["OPENAI_API_KEY"]
apify_api_key = os.environ["APIFY_API_TOKEN"]

apify = ApifyWrapper(open_api_key)

def crawl_website_links():
    """Combs through the various links provided and collects relevant data from that link"""

    # skills, work experience and certifications
    # grab as much as you can from linkedIn and job urls (eg glassdoor, handshake, indeed)

    # Prepare the Actor input
    run_input = {
        "startUrls": [{ "url": "https://www.linkedin.com/in/elijuwon-mitchell-99475314b/" }],
        "instructions": """Gets the post with the most points from the page and returns it as JSON in this format: 
    postTitle
    postUrl
    pointsCount""",
        "model": "gpt-3.5-turbo",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "linkSelector": "a[href]",
        "initialCookies": [],
        "proxyConfiguration": { "useApifyProxy": True },
        "targetSelector": "",
        "removeElementsCssSelector": "script, style, noscript, path, svg, xlink",
        "skipGptGlobs": [],
        "schema": {
            "type": "object",
            "properties": {
                "Name": {
                    "type": "string",
                    "description": "Person Name",
                },
                "Birthday": {
                    "type": "string",
                    "description": "The Birthday of the person",
                },
                "Address" :{
                    "city": {
                        "type":"string",
                        "description":"City of Residence"
                    },
                    "postal code": {
                        "type":"string",
                        "description":"Postal Code of City"
                    },
                    "country": {
                        "type":"string",
                        "description":"Country where person lives"
                    },
                }
            },
            "required": [
                "Name",
                "Birthday",
                "Address",
            ],
        },
        "schemaDescription": "Used to grab three points of refence for a persons description",
    }

    loader = apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input=run_input,
        dataset_mapping_function=lambda item: Document(
            page_content=item["text"] or "", metadata={"source": item["url"]}
        ),
    )
    index = VectorstoreIndexCreator().from_loaders([loader])
    query = "What is the name, birthday and or address found on the url given"
    result = index.query_with_sources(query)
    return result




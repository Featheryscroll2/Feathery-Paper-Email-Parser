from urllib.parse import urlparse
from typing import List
import requests
import json


def get_domain(url: str):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def get_actual_url(link: str):
    # Set the API endpoint URL
    url = "https://tap-api-v2.proofpoint.com/v2/url/decode"

    # Set the request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Set the request payload
    payload = {
        "urls": [
            link
        ]
    }

    try:
        # Send the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload)).json()

        # Access the decoded URL from the dictionary
        decoded_url = response['urls'][0]['decodedUrl']
        return {
            "error": False,
            "url": decoded_url,
            "domain": get_domain(decoded_url)
        }
    except Exception as e:
        print(f"Error occurred while getting actual URL for {link}: {e}")
        return {
            "error": True,
            "msg": f"Error occurred while getting actual URL for {link} using Proof Point"
        }


def get_url_domain(links: List[str]):
    link_list = []
    domain_list = []
    error_list = []
    for link in links:
        real_link = ''
        real_domain = ''
        # checks if link is encoded
        if link.startswith("mailto:"):
            continue
        elif link.startswith("https://urldefense.com") and len(link) != len("https://urldefense.com"):
            result = get_actual_url(link)
            if result["error"]:
                error_list.append(result["msg"])
            else:
                real_link = result["url"]
                real_domain = result["domain"]
        else:
            real_link = link
            real_domain = get_domain(link)
        # check if domain or link is in the list before add
        if real_domain != '' and real_domain not in domain_list:
            domain_list.append(real_domain)
        if real_link != '' and real_link not in link_list:
            link_list.append(real_link)
    return {
        "links": link_list,
        "domains": domain_list,
        "errors": error_list
    }

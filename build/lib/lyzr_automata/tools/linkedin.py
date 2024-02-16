from dataclasses import Field
import json
from typing import Optional
from pydantic import BaseModel

import requests

from lyzr_automata.tools.tool_base import Tool


def post_image_and_text(
    owner: str, token: str, title: str, file_path: str, text_content: str
):
    """
    Posts an article on LinkedIn with an image thumbnail.

    :param token: str. LinkedIn OAuth token.
    :param owner: str. LinkedIn person ID (e.g., 'urn:li:person:XXXX').
    :param title: str. Article title.
    :param description: str. Article description.
    :param source: str. URL of the article source.
    :param file_path: str. Local file path of the image to be used as a thumbnail.
    """
    # Initialize the upload to get the upload URL and image URN
    init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    headers = {
        "LinkedIn-Version": "202401",
        "X-RestLi-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    init_data = json.dumps({"initializeUploadRequest": {"owner": owner}})
    init_response = requests.post(init_url, headers=headers, data=init_data)
    if init_response.status_code != 200:
        raise Exception(f"Failed to initialize upload: {init_response.text}")

    init_response_data = init_response.json()["value"]
    upload_url = init_response_data["uploadUrl"]
    image_urn = init_response_data["image"]

    # Upload the file
    with open(file_path, "rb") as f:
        upload_response = requests.post(upload_url, files={"file": f})
        if upload_response.status_code not in [200, 201]:
            raise Exception(f"Failed to upload file: {upload_response.text}")

    # Create the post with the uploaded image URN as thumbnail
    post_url = "https://api.linkedin.com/rest/posts"
    post_data = json.dumps(
        {
            "author": owner,
            "commentary": text_content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "content": {
                "media": {
                    "title": title,
                    "id": image_urn,
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
    )
    post_response = requests.post(post_url, headers=headers, data=post_data)
    if post_response.status_code in [200, 201]:
        return "Posted Successfully"
    else:
        raise Exception(f"Failed to post article: {post_response.text}")


class LinkedInPostInput(BaseModel):
    title: str
    file_path: str
    text_content: str


class LinkedInPostOutput(BaseModel):
    success: bool
    message: Optional[str]
    article_urn: Optional[str]

from ast import List
from pydantic import BaseModel
import requests
import json
import re

import re

def sanitize_to_strict_alphanumeric(input_value, ascii_only=True):
    """
    Converts any input to a strictly alphanumeric string, removing spaces and enforcing ASCII-only characters if desired.

    :param input_value: The input to be sanitized.
    :param ascii_only: Whether to enforce ASCII-only characters.
    :return: A sanitized string with only alphanumeric characters.
    """
    # Convert the input to a string first
    str_value = str(input_value)
    
    # If enforcing ASCII-only characters, encode and decode to remove non-ASCII characters
    if ascii_only:
        str_value = str_value.encode('ascii', 'ignore').decode('ascii')
    
    # Use regular expressions to keep only alphanumeric characters
    sanitized_str = re.sub(r'[^a-zA-Z0-9]', '', str_value)
    
    return sanitized_str
    
def create_devto_article(api_key, title, published, markdown_body_content, tags, series):
    if series == None:
        series = title
    tags = [sanitize_to_strict_alphanumeric(tag) for tag in tags]
    """
    Create an article on dev.to.

    Parameters:
    - api_key (str): The API key for authentication.
    - title (str): The title of the article.
    - published (bool): Whether the article should be published immediately.
    - content (str): The content of the article in Markdown format.
    - tags (list): A list of tags for the article.
    - series (str): The series the article belongs to.

    Returns:
    - dict: The JSON response from the API.
    """
    # URL for the dev.to articles API
    url = 'https://dev.to/api/articles'
    
    # Headers to be sent with the POST request
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key,
    }
    tags = tags[0:4]
    # Data (payload) to be sent in the POST request
    data = {
        'article': {
            'title': title,
            'published': published,
            'body_markdown': markdown_body_content,
            'tags': tags,
            'series': series,
        },
    }
    
    # Making the POST request
    response = requests.post(url, headers=headers, json=data)
    
    # Parsing the JSON response
    response_json = response.json()
    
    # Returning the response
    return response_json

class DevToArticleInput(BaseModel):
    title: str
    markdown_body_content: str 
    tags: list[str]
    series: str

class DevToArticleOutput(BaseModel):
    url:str
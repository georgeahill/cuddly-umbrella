import requests


class ConnectionHelperException(Exception):
    def __init__(self, code, message):
        super().__init__("Code: " + code + "\n" + message)


# Headers to send to Wikipedia API; this is a requirement.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
wiki_base_url = "https://en.wikipedia.org/w/rest.php/v1"


def get_wikipedia_data(query):
    """Get the relevant fields from a Wikipedia search

    Args:
        query (str): The search query

    Returns:
        title (str): The title of the wikipedia article (allows for correction of mistakes)
        key (str): The wikipedia-provided unique key
        description (str): A short description of the article
        text (str): The full body text of the article
        image (file): The raw image file data, if available
        image_url (str): The url for the image
        width (int): The width of the thumbnail image (if applicable)
        height (int): The height of the thumbnail image (if applicable)
    """
    title = None
    key = None
    image = None
    # Default the URL to a blank 1x1 GIF in base64
    image_url = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
    width = None
    height = None
    text = None
    description = None

    # Search request
    r = requests.get(f"{wiki_base_url}/search/page?q={query}&limit=1", headers=headers)

    if r.status_code != 200:
        raise ConnectionHelperException(r.status_code, r.content)

    page_obj = r.json()['pages'][0]

    key = page_obj['key']
    title = page_obj['title']

    if page_obj["description"] is None:
        page_obj["description"] = page_obj["excerpt"] + "..."
    if page_obj["description"] is None:
        page_obj["description"] = "<em>Description not available</em>"

    description = page_obj['description']

    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/page/{key}", headers=headers)

    if r.status_code != 200:
        raise ConnectionHelperException(r.status_code, r.content)

    text = r.json()["source"]

    if page_obj is None:
        raise ConnectionHelperException(200, r.content)

    # if there's a thumbnail provided
    if 'thumbnail' in page_obj and page_obj["thumbnail"] is not None and "url" in page_obj["thumbnail"]:
        image_url = "https:" + page_obj["thumbnail"]["url"]
        image_req = requests.get(image_url, headers=headers)
        # app.logger.debug(image_url, image_req)
        if image_req.status_code != 200:
            image = None
        else:
            image = image_req.content

        width = page_obj['thumbnail']['width']
        height = page_obj['thumbnail']['height']
        

    return title, key, description, text, image, image_url, width, height


def get_mask(image):
    """ Get binarized threshold mask
    
    Args:
        image (raw): The image to binarize, in any supported format
        
    Returns:
        image_data (np.ndarray): The binarized image, pixel-wise, from the API
    """
    # call the web service
    r = requests.post("http://imageprocess:8000/threshold/create", files={"data": image})

    if r.status_code != 200:
        raise ConnectionHelperException(r.status_code, r.content)

    image_data = r.json()["mask"]

    return image_data


def get_wordcloud(text, width=None, height=None, mask=None):
    """ Get wordcloud from various options

    Returns:
        svg (str): str containing SVG representation of wordcloud
    """
    options = {
        "text": text,
        "state": "no_image"
    }
    if width is not None and height is not None:
        options["image_width"] = width
        options["image_height"] = height
        state = "no_mask"

    if mask:
        options["state"] = "mask"
        options["mask"] = mask

    r = requests.post("http://wordcloud:8000/wordcloud", json=options)

    if r.status_code != 200:
        # try again, without a mask
        del options["mask"]
        options["state"] = "no_mask"
        r = requests.post("http://wordcloud:8000/wordcloud", json=options)
        if r.status_code != 200:
            # now fail
            raise ConnectionHelperException(r.status_code, r.content)

    return r.json()['cloud']
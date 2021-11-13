from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import send_from_directory
from bs4 import BeautifulSoup
import re
import logging

import requests

import connection_helper

app = Flask(__name__)

# TODO: generate this on-the-fly using Docker
app.config["SECRET_KEY"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA "


def preprocess_text(source):
    """ Clean text from wikitags etc.

    Args:
        source (str): The text to preprocess

    Returns:
        text (str): The processed text
    """
    soup = BeautifulSoup(source, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()
 
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    text = re.sub(r"\{\{.+\}\}", "", text)
    text = re.sub(r"\[\[.+\]\]", "", text)
    text = re.sub(r"==.+==", "", text)

    return text


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/<string:page>")
@app.route("/", methods=["POST", "GET"])
def index(page=None):
    if request.method == "POST":
        return redirect("/" + request.form.get("query"))

    if page is None:
        # "/"
        return render_template("index.html")

    # Get all wiki data from search
    try:
        title, key, description, text, image, image_url, width, height = connection_helper.get_wikipedia_data(page)
    except ConnectionHelperException:
        return render_template('index.html', error="Page not found boo! Try again xoxo")


    # Preprocess text
    text = preprocess_text(text)
    error = None

    # only call this service if necessary/possible
    if image:
        try:
            mask = connection_helper.get_mask(image)
        except:
            mask = None

        try:
            image_data = connection_helper.get_wordcloud(text, width, height, mask)
        except:
            image_data = None
            error = "Something went wrong generating the wordcloud"
    else:
        # no mask available
        try:
            image_data = connection_helper.get_wordcloud(text)
        except:
            image_data = None
            error = "Something went wrong generating the wordcloud"

    return render_template(
        "index.html",
        image_data=image_data,
        source_image_data=image_url,
        error=error,
        title=title,
        description=description,
        key=key,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
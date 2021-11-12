from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import send_from_directory
import requests
from bs4 import BeautifulSoup
import re
import logging

app = Flask(__name__)

app.config["SECRET_KEY"] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA "


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

    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # Call wikipedia - get text
    r = requests.get(
        f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={page}&limit=1",
        headers=headers
    )
    try:
        page_obj = r.json()["pages"][0]
    except:
        return render_template("index.html", error="Page not found boo! Try again xoxo")

    if not page_obj:
        return render_template("index.html", error="Page not found boo! Try again xoxo")

    if (
        "thumbnail" in page_obj
        and page_obj["thumbnail"] is not None
        and "url" in page_obj["thumbnail"]
    ):
        image_url = "https:" + page_obj["thumbnail"]["url"]
        image_req = requests.get(image_url, headers=headers)
        # app.logger.debug(image_url, image_req)
        if image_req.status_code != 200:
            image = None
        else:
            image = image_req.content
    else:
        image_url = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
        image = None

    page_title = page_obj["key"]

    if page_obj["description"] is None:
        page_obj["description"] = page_obj["excerpt"] + "..."
    if page_obj["description"] is None:
        page_obj["description"] = "<em>Description not available</em>"

    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/page/{page_title}", headers=headers)

    source = r.json()["source"]
    soup = BeautifulSoup(source, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
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

    # Call Ben's API with wikipedia

    try:
        if image:
            r = requests.post("http://imageprocess:8000/process", files={"data": image})
            # reconcile formats here
            image_data = r.json()["mask"]
            # image_data_clean = [[cell, cell, cell] for row in image_data for cell in row]

            r = requests.post(
                "http://wordcloud:8000/wordcloud",
                json={
                    "wikitext": text,
                    "mask": image_data,
                    "image_width": page_obj["thumbnail"]["width"],
                    "image_height": page_obj["thumbnail"]["height"],
                    "state": "mask",
                },
            )
            if r.status_code != 200:
                r = requests.post(
                    "http://wordcloud:8000/wordcloud",
                    json={
                        "wikitext": text,
                        "image_width": page_obj["thumbnail"]["width"],
                        "image_height": page_obj["thumbnail"]["height"],
                        "state": "no_mask",
                    },
                )
        else:
            r = requests.post(
                "http://wordcloud:8000/wordcloud",
                json={
                    "wikitext": text,
                    "state": "no_image",
                },
            )
        image_data = r.json()['cloud']
        error = None
    except Exception as ex:
        print(ex)
        image_data = None
        error = "Something went wrong generating the wordcloud"

    return render_template(
        "index.html",
        image_data=image_data,
        source_image_data=image_url,
        error=error,
        page=page_obj,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
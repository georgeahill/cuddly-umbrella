from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
app = Flask(__name__)

app.config['SECRET_KEY'] = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA '


@app.route("/<string:page>")
@app.route("/", methods=["POST", "GET"])
def index(page=None):
    if request.method == "POST":
        print(request.form.to_dict())
        return redirect("/" + "dog")
    
    if page is None:
        # "/"
        return render_template("index.html")

    # Call wikipedia - get text
    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={page}&limit=1")
    try:
        page_obj = r.json()["pages"][0]
    except:
        pass

    page_title = page_obj['key']

    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/page/{page_title}")

    source = r.json()["source"]
    soup = BeautifulSoup(source, features="html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    text = re.sub(r"\{\{.+\}\}", '', text)
    text = re.sub(r"\[\[.+\]\]", '', text)
    text = re.sub(r"==.+==", '', text)

    # Call Ben's API with wikipedia

    try:
        r = requests.post("http://localhost:5000", data={"data": text})
        image_data = r.json()["image"]
        error = None
    except:
        image_data = None
        error = "Something went wrong generating the wordcloud"

    return render_template("index.html", image_data=image_data, error=error)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
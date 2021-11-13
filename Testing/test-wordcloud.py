import requests
import timeit
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def test_wordcloud(image_url, page, type):
    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/page/{page}", headers=headers)

    source = r.json()["source"]
    soup = BeautifulSoup(source, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    mask = None
    if type == 0:
        image_req = requests.get(image_url, headers=headers)
        image = image_req.content

        if image_req.status_code != 200:
            return None

        r = requests.post("http://localhost:8000/threshold/create", files={"data": image})

        if r.status_code != 200:
            return r.content

        mask = r.json()['mask']
    
    if type == 0:
        start = timeit.default_timer()
        r = requests.post(
                    "http://localhost:8001/wordcloud",
                    json={
                        "text": text,
                        "mask": mask,
                        "state": "mask",
                    },
                )
        end = timeit.default_timer()
    elif type == 1:
        start = timeit.default_timer()
        r = requests.post(
                    "http://localhost:8001/wordcloud",
                    json={
                        "text": text,
                        "state": "no_mask",
                    },
                )
        end = timeit.default_timer()
    elif type == 2:
        start = timeit.default_timer()
        r = requests.post(
                    "http://localhost:8001/wordcloud",
                    json={
                        "text": text,
                        "state": "no_image",
                    },
                )
        end = timeit.default_timer()

    if r.status_code != 200:
        return r.content

    return end - start

image_urls = [
    "https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@1.5x.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Frederik_Willem_de_Klerk%2C_1990.jpg/250px-Frederik_Willem_de_Klerk%2C_1990.jpg",
    ]

print(test_wordcloud(image_urls[0], "Wikipedia", type=0))
print(test_wordcloud(image_urls[1], "Frederik Willem de Klerk", type=0))
print(test_wordcloud(image_urls[1], "Jeunesse Esch", type=1))
print(test_wordcloud(image_urls[1], "Two Concepts of Liberty", type=1))
print(test_wordcloud(image_urls[1], "1980 Pontins Camber Sands", type=2))
print(test_wordcloud(image_urls[1], "Intermontane Belt", type=2))


import requests
import timeit

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def test_imageproc(image_url):
    image_req = requests.get(image_url, headers=headers)
    image = image_req.content

    start = timeit.default_timer()
    if image_req.status_code != 200:
        return None
    r = requests.post("http://localhost:8000/threshold/create", files={"data": image})
    end = timeit.default_timer()

    if r.status_code != 200:
        return r.content

    return end - start

image_urls = [
    "https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@1.5x.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Frederik_Willem_de_Klerk%2C_1990.jpg/250px-Frederik_Willem_de_Klerk%2C_1990.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2006_Ojiya_balloon_festival_011.jpg/200px-2006_Ojiya_balloon_festival_011.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2006_Ojiya_balloon_festival_011.jpg/133px-2006_Ojiya_balloon_festival_011.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Mahatma-Gandhi%2C_studio%2C_1931.jpg/440px-Mahatma-Gandhi%2C_studio%2C_1931.jpg",
]

for image in image_urls:
    print(test_imageproc(image))
import requests
import timeit

def test_wikipedia(page):
    start = timeit.default_timer()

    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # Call wikipedia - get text
    r = requests.get(
        f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={page}&limit=1",
        headers=headers
    )

    if r.status_code != 200:
        return None

    r = requests.get(f"https://en.wikipedia.org/w/rest.php/v1/page/{page}", headers=headers)


    if r.status_code != 200:
        return None

    end = timeit.default_timer()

    return end - start

terms = [
    "Hot-air balloon",
    "Titanic",
    "Zyzzyx",
    "Fleet",
    "Monster Energy"
]

for term in terms:
    print(test_wikipedia(term))
# Wikipedia API Specification
Reference taken from [here](https://www.mediawiki.org/wiki/API:REST_API/Reference)

root is `https://en.wikipedia.org/w/rest.php/v1`

## Page search
`/search/page?q={search query}&limit={Limit (1)}`

### Returns:
```json
{
  "id": 38930,
  "key": "Jupiter",
  "title": "Jupiter",
  "excerpt": "<span class=\"searchmatch\">Jupiter</span> is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half",
  "description": "fifth planet from the Sun and largest planet in the Solar System",
  "thumbnail": {
    "mimetype": "image/jpeg",
    "size": null,
    "width": 200,
    "height": 200,
    "duration": null,
    "url": "//upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/200px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg"
  }
}```


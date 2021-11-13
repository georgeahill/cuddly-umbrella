# WordCloud API Specification

## Build and Run
### With Docker

Ensure docker is installed. Run `docker build -t wordcloud . && docker run -p 5000:8000 wordcloud`

root is `localhost:5000` by default. 

#
## WordCloud
`/wordcloud`

### Returns:
string containing WordCloud image in SVG format

### Params:

**text** _(Required)_ -  The text from which to build the word cloud

**state** _(Required)_ - `mask` creates an image with black text in the shape of the passed mask. `no_mask` creates an image with black text and no mask. `no_image` creates an image with colourful text and no mask.

**mask** - A bitmap array of the mask image. Only required when `state='mask'`

**image_width** - The width (in pixels) of the wordcloud to return (default 500)

**image_height** - The height (in pixels) of the wordcloud to return (default 500)

**max_words** - The max number of words to show in the wordcloud (default 100)

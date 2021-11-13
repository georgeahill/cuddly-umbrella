# WordCloud API Specification

root is `localhost:5000`

#
## WordCloud
`/wordcloud`

### Returns:
string containing WordCloud image in Base64 format

### Params:

**text** - _(Required)_ The text from which to build the wordcloud

**state** - _(Required)_ **_'mask'_** creates an image with black text in the shape of the passed mask. **_'no_mask'_** creates an image with black text and no mask. **_'no_image'_** creates an image with colourful text and no mask.

**mask** - _(Required)_ A bitmap array of the mask image

**image_width** - The width (in pixels) of the wordcloud to return (default 500)

**image_height** - The height (in pixels) of the wordcloud to return (default 500)

**max_words** - The max number of words to show in the wordcloud (default 100)

# WordCloud API Specification

root is `localhost:5000`

#
## WordCloud with no mask
`/no_mask`

### Returns:
string containing WordCloud image in Base64 format

### Params:

**text** - _(Required)_ The text from which to build the wordcloud

**image_width** - The width (in pixels) of the wordcloud to return (default 500)

**image_height** - The height (in pixels) of the wordcloud to return (default 500)

**max_words** - The max number of words to show in the wordcloud (default 100)

#
## WordCloud with mask
`/mask`

### Returns:
string containing WordCloud image in Base64 format

### Params:

**text** - _(Required)_ The text from which to build the wordcloud

**mask** - _(Required)_ A bitmap array of the mask image

**image_width** - The width (in pixels) of the wordcloud to return (default 500)

**image_height** - The height (in pixels) of the wordcloud to return (default 500)

**max_words** - The max number of words to show in the wordcloud (default 100)
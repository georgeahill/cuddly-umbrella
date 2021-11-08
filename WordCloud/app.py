from flask import Flask, request
import re
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import base64
from io import BytesIO
import os


#Define a list of stop words
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
    'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
    'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

app = Flask(__name__)

@app.route("/no_mask", methods = ["POST"])
def wordcloud_no_mask():
    #get the data from the POST command and store into a variable
    data = request.get_json()
    wikitext = data["wikitext"]
    if "image_width" in data:
        imagewidth = data["image_width"]
    else:
        imagewidth = 500
    if "image_height" in data:
        imageheight = data["image_height"]
    else:
        imageheight = 500
    if "max_words" in data:
        max_words = data["max_words"]
    else:
        max_words = 100

    #Clean the input of any punctuation and put into a string separated by single spaces
    cleanedInput = re.sub(r"""
               [–()-/*'",.;@#?!&$\s]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               wikitext, flags=re.VERBOSE)

    print(cleanedInput)


    #generate the word cloud from text
    cloud = WordCloud(font_path=os.getcwd() + '/Avenir Regular/Avenir Regular.ttf',
                    width=imagewidth,
                      height=imageheight,
                      max_words=max_words,
                      colormap='cool',
                      background_color='#282828',
                      stopwords=stopwords,
                      collocations=False,
                      min_word_length=2).generate_from_text(cleanedInput)

    #Put this into an image file
    im = Image.fromarray(cloud.to_array())

    #convert the image into a base64 string
    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = "data:image/png;base64," + str(base64.b64encode(buffered.getvalue()))[2:-1]

    #return this string to the client
    return img_str

@app.route("/mask", methods = ["POST"])
def wordcloud_mask():
    #get the data from the POST command and store into variables
    data = request.get_json()
    wikitext = data["wikitext"]
    mask = data["mask"]
    if "image_width" in data:
        imagewidth = data["image_width"]
    else:
        imagewidth = 500
    if "image_height" in data:
        imageheight = data["image_height"]
    else:
        imageheight = 500
    if "max_words" in data:
        max_words = data["max_words"]
    else:
        max_words = 100

    #Clean the input of any punctuation and put into a string separated by single spaces
    cleanedInput = re.sub(r"""
               [–()-/*'",.;@#?!&$\s]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               wikitext, flags=re.VERBOSE)

    #create a variable to store the colourway from the image mask
    colors = ImageColorGenerator(mask)

    #generate the word cloud from text
    cloud = WordCloud(font_path=os.getcwd() + '/Avenir Regular/Avenir Regular.ttf',
                    width=imagewidth,
                    height=imageheight,
                    max_words = max_words,
                    stopwords = stopwords,
                    mask=mask,
                    background_color='white',
                    color_func=colors,
                    collocations=False,
                    min_word_length=2).generate_from_text(cleanedInput)

    #Put this into an image file
    im = Image.fromarray(cloud.to_array())

    #convert the image into a base64 string
    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = "data:image/png;base64," + str(base64.b64encode(buffered.getvalue()))[2:-1]

    #return this string to the client
    return img_str
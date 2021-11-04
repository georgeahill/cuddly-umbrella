from flask import Flask, request
import re
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import base64
from io import BytesIO


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
    data = request.get_json()
    print(data)

    wikitext = data["wikitext"]

    cleanedInput = re.sub(r"""
               [,.;@#?!&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               wikitext, flags=re.VERBOSE)




    #generate the word cloud from text
    cloud = WordCloud(width=400,
                      height=330,
                      max_words=150,
                      colormap='tab20c',
                      stopwords=stopwords,
                      collocations=True).generate_from_text(cleanedInput)

    im = Image.fromarray(cloud.to_array())

    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str

@app.route("/mask", methods = ["POST"])
def wordcloud_mask():
    data = request.get_json()
    print(data)

    wikitext = data["wikitext"]
    mask = data["mask"]

    cleanedInput = re.sub(r"""
               [,.;@#?!&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               " ",          # and replace it with a single space
               wikitext, flags=re.VERBOSE)

    colors = ImageColorGenerator(mask)

    cloud = WordCloud(width=400,
                    height=330,
                    max_words = 50,
                    stopwords = stopwords,
                    mask=mask,
                    background_color='white',
                    color_func=colors).generate_from_text(data)

    im = Image.fromarray(cloud.to_array())

    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str
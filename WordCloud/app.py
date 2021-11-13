import os
import logging
import re

from flask import Flask
from flask_restful import Api, Resource, reqparse
import numpy as np
from werkzeug.exceptions import default_exceptions
from wordcloud import WordCloud

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("text", type=str, location="json", required=True, help="{error_msg}")
parser.add_argument("state", type=str, location="json", required=True, choices=('mask', 'no_mask', 'no_image'), help="{error_msg}")
parser.add_argument("mask", type=list, location="json", help="{error_msg}")
parser.add_argument("image_width", type=int, location="json", help="{error_msg}", default=500)
parser.add_argument("image_height", type=int, location="json", help="{error_msg}", default=500)
parser.add_argument("max_words", type=int, location="json", help="{error_msg}", default=100)

# Define a list of stop words
stopwords = set([
    "i",    "me",    "my", "myself", "we", "our", "ours", "ourselves", "you", 
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", 
    "their", "theirs", "themselves", "what", "which", "who", "whom", "this", 
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", 
    "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", 
    "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
    "of", "at", "by", "for", "with", "about", "against", "between", "into", 
    "through", "during", "before", "after", "above", "below", "to", "from", 
    "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", 
    "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", 
    "will", "just", "don", "should", "now", "www", "http", "https", "http", 
    "org", "com", "net", "jpg", "edu", "pdf", "png", "infobox", "url", "file", 
    "web", "cite", "journal", "id", "ogg", "XML", "html"
])

def colorfunc(*args, **kwargs):
    return 'hsl(0, 0, 0)'

class WordCloudResource(Resource):
    def post(self):
        args = parser.parse_args()

        # Clean the input of any punctuation and put into a string separated by single spaces
        cleanedInput = re.sub(
            r"""
                [–()-/*'",.;@#?!&$\s]+  # Accept one or more copies of punctuation
                \ *           # plus zero or more copies of a space,
                """,
            " ",  # and replace it with a single space
            args['text'],
            flags=re.VERBOSE,
        )

        # generate the word cloud from text
        if args["state"] == 'mask':
            cloud = WordCloud(
                font_path=os.getcwd() + "/Avenir Regular/Avenir Regular.ttf",
                width=args['image_width'],
                height=args['image_height'],
                max_words=args['max_words'],
                stopwords=stopwords,
                mask=np.array(args['mask']),
                background_color=None,
                color_func=colorfunc,
                collocations=False,
                contour_width=5,
                contour_color="black",
                min_word_length=2,
            ).generate_from_text(cleanedInput)
        elif args["state"] == 'no_mask':
            cloud = WordCloud(
                font_path=os.getcwd() + "/Avenir Regular/Avenir Regular.ttf",
                width=args['image_width'],
                height=args['image_height'],
                max_words=args['max_words'],
                color_func=colorfunc,
                background_color="#282828",
                stopwords=stopwords,
                collocations=False,
                min_word_length=2,
            ).generate_from_text(cleanedInput)
        else:
            cloud = WordCloud(
                font_path=os.getcwd() + "/Avenir Regular/Avenir Regular.ttf",
                width=args['image_width'],
                height=args['image_height'],
                max_words=args['max_words'],
                colormap = "cool",
                background_color="#282828",
                stopwords=stopwords,
                collocations=False,
                min_word_length=2,
            ).generate_from_text(cleanedInput)

        # Put this into an image file
        im = cloud.to_svg(embed_font=True)

        # return this string to the client
        return {"cloud": im}


api.add_resource(WordCloudResource, '/wordcloud')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
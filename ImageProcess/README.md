# ImageProcess API

Produce a binarized threshold mask from a provided image.

## Build and Run

### With Docker:
`docker build -t imageproc . && docker run -p 8000:8000 imageproc`

### With Flask:

You only need to run pip once:
`pip3 install -r requirements.txt`

Then to run each time do
`flask run`

You will need to ensure the other services are running too. 

Flask will then provide you a URL and port to access. Refer to the documentation (submitted as part of the report) on how to use the API. 

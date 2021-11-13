# Client

This client integrates the 3 APIs for this project. 

## Build and Run

### With Docker:
`docker build -t client . && docker run -p 8000:8000 client`

### With Flask:

You only need to run pip once:
`pip3 install -r requirements.txt`

Then to run each time do
`flask run`

You will need to ensure the other services are running too. 

Flask will then provide you a URL and port to access. 
# Follow Canvas's OAuth2 flow to get the access token from Canvas API key and LTI key
# Reference: https://canvas.instructure.com/doc/api/file.oauth.html#oauth2-flow
# TODO: Define the endpoints for the OAuth2 flow

from main import config, app


@app.route("/canvas_oauth/", methods=["GET"])
def get_oauth_code():
    pass



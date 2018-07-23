import logging
from flask import Flask, request, Response, g
import webbrowser
from pinkdeck.core import config

# Turn off Flask logging
werklog = logging.getLogger("werkzeug")
werklog.setLevel(logging.ERROR)

log = logging.getLogger("pinkdeck.core.server")
log.setLevel(config.LOG_LEVEL)

# XXX: Global state really sucks, and can probably be fixed with some changes.
global oauth
oauth = None

def create_server():
    endpoint = config.AUTHORIZE_URL.format(config.CLIENT_ID)

    log.info("Starting server")

    app = Flask("pinkdeck")

    def after_this_request(func):
        if not hasattr(g, 'call_after_request'):
            g.call_after_request = []
        g.call_after_request.append(func)
        return func

    @app.after_request
    def per_request_callbacks(response):
        for func in getattr(g, 'call_after_request', ()):
            response = func(response)
        return response

    def shutdown_server():
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            return None
        func()

    @app.route("/")
    def flask_index():
        return """
        <script>
            var h = window.location.hash;
            if(h) {
                h = h.substring(1, h.length);
                window.location = "/authorize?" + h;
            } else {
                document.write("Something went wrong, sorry!");
            }
        </script>
        """

    @app.route("/authorize")
    def flask_authorize():
        log.info("Got twitch auth key!")
        global oauth
        items = map(lambda x: x.split("="), request.query_string.decode().split("&"))
        for key, value in items:
            if key == "access_token":
                oauth = value
        # Couldn't get OAuth value
        if not oauth:
            @after_this_request
            def r(*args, **kwargs):
                shutdown_sever()
                log.error("Couldn't get proper authorization, please restart the application and try again.")
                return Response("""<h1>Sorry</h1><p>We couldn't get proper authorization, please restart the application and try again.""")
        else:
            @after_this_request
            def r(*args, **kwargs):
                shutdown_server()
                return Response("""<script>window.open('', '_self').close()</script>""")
        # We still need to return "something" so Flask treats this view properly, I think
        return ""

    # Gotta get the user to open this somehow.
    webbrowser.open_new(endpoint)

    app.run(port=config.WEB_SERVER_PORT)
    log.info("Server ending")

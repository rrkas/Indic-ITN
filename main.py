import falcon
from wsgiref.simple_server import make_server
from modules.server.auth_middleware import AuthMiddleware
from modules.server.serve_itn import ServeITN

app = falcon.App(
    middleware=[
        AuthMiddleware(),
    ],
)

app.add_route("/ITN", ServeITN())

if __name__ == "__main__":
    httpd = make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()

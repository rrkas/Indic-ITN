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
    host = "127.0.0.1"
    port = 8000
    httpd = make_server(host, port, app)
    print(f"Server listening at: {host}:{port}")
    httpd.serve_forever()

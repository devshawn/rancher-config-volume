import socket
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class MockServerRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, mock_name, *args, **kwargs):
        self.mock_name = mock_name
        self.retry_counter = 0
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            relevant_path = self.path.replace("/2015-07-25/self/service/metadata/", "").split("/")
            folder = relevant_path[1]
            operation = relevant_path[-1]

            if folder == "0-success":
                if operation == "path":
                    self.response(200, "plain/text", "/config/app/config.yaml")
                else:
                    self.response(200, "plain/text", "content")
            elif folder == "1-success-two":
                if operation == "path":
                    self.response(200, "plain/text", "/my/new/config/test.json")
                else:
                    self.response(200, "plain/text", "{}")
            elif folder == "2-404-key":
                self.response(404, "plain/text", "Not Found")
            elif folder == "3-500-error":
                self.response(500, "plain/text", "Internal Server Error")
            else:
                self.response(500, "plain/text", "Exception")

        except Exception as ex:
            print("Error while handling mock GET request: {}".format(ex))
            self.response(500, "plain/text", "Exception")

    def response(self, status_code, content_type, payload):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(payload.encode('utf-8'))


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, mock_name):
    handler = partial(MockServerRequestHandler, mock_name)
    mock_server = HTTPServer(('localhost', port), handler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
    print("\nMock rancher metadata server running on port: {}".format(port))

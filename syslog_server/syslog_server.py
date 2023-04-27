import socketserver
import logging
import json

with open("config.json", "r") as f:
    config = json.load(f)

HOST = config["Host"]
PORT = config["Port"]

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    filename="app_logs.txt", filemode="a")


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = bytes.decode(self.request[0].strip())
        logging.info(data)


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except(IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down server...")

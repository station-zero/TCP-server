import socket
import pytz # Module for parsing timezone shenanigans
from datetime import datetime

PORT = 16000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))
s.listen(5)

session = {
    "client_header": "",
    "client_ip": "",
    "response_code": "",
    "size": ""
}

def generate_log_datetime():
    log_date = datetime.now(pytz.timezone("Europe/Copenhagen")).strftime("%Y-%b-%d %H:%M:%S %z")
    return log_date

def generate_response_datetime():
    response_date = datetime.now(pytz.timezone("Europe/Copenhagen")).strftime("%a, %Y-%b-%d %H:%M:%S %Z")
    return response_date

def log_it():
    with open("log.txt", "a") as log_file:
        client_ip = session["client_ip"]
        http_header = session["client_header"]
        size = session["size"]
        date = generate_log_datetime()
        log_file.write(f"{client_ip} - - {date} \"{http_header}\" {size} \n")

def parse_content_type(filetype):
    match filetype:
        case "html":
            return "Content-Type: text/html"
        case "png":
            return "Content-Type: image/png"
        case "css":
            return "Content-Type: text/css"
        case "js":
            return "Content-Type: text/javascript"
        case _:
            return "Content-Type: text/html" 

def send_reply(status_code, body, filetype):
    if status_code == "404":
        header = "HTTP/1.1 404 NOT FOUND\r\n"

    elif status_code == "GET":
        header = "HTTP/1.1 200 OK\r\n"

    elif status_code == "400":
        header = "HTTP/1.1 400 Bad Request\r\n"

    header += f"Date: {generate_response_datetime()}\r\n"
    header += parse_content_type(filetype) + "\r\n"
    header += "\r\n" # Finishing the header

    print("Request headers: " + payload)

    payload = header + body #data in response
    payload_encoded = payload.encode()
    session["size"] = len(payload_encoded)

    log_it()

    connection.sendto(payload_encoded, client)
    print("send response to client")

def unpack_header(header):
    response_txt = ""

    try:
        header_lines = header.split("\r\n")
        request = header_lines[0].split(" ")
        methode = request[0]
        file = request[1]
        httpv = request[2]
        #print("Filetype: " + filetype)
        print("request from: " + client[0])
        print("methode: " + methode)
        print("file: " + file)
        print("http v:" + httpv)
    except:
        print("Bad request from: " + client[0])
        methode = "400"

    if methode == "GET":
        if file == "/":
            file = "/index.html"
        try:
            with open(file[1:]) as f:
                response_txt = f.read()
        except:
            methode = "404"
    else:
        methode = "400"

    try:
        filetype = file.split(".")[1] #only works when we specify the filetype in uri...
    except:
        filetype = ""
        methode = "400"

    session["client_header"] = header_lines[0]
    session["client_ip"] = client[0]
    session["response_code"] = methode

    send_reply(methode, response_txt, filetype)

while True:
    connection , client = s.accept()
    data = connection.recv(2048).decode()
    print("Data: " + data)
    if data != "":
        unpack_header(data)
        connection.close()
s.close() #todo: a function to call it
import socket
from datetime import datetime

PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))
s.listen(5)

session = {
    "client_header": "",
    "client_ip": "",
    "response_code": "",
}

def log_it(client_ip, size, http_header):
    print("log file")
    try:
        with open("log.txt", "a") as log_file:
            date = str(datetime.now())
            log_file.write(f"{client_ip} - - {date} \" {http_header}\" {size}")
    except:
        pass

def send_reply(status_code, body):
    if status_code == "404":
        header = "HTTP/1.1 404 Not Found\r\n\r\n"

    elif status_code == "GET":
        header = "HTTP/1.1 200 OK\r\n"
        header += "Content-Type: text/html\r\n\r\n"

    elif status_code == "400":
        header = "HTTP/1.1 400 Bad Request\r\n"
        
    payload = header + body
    payload_encoded = payload.encode()
    size = len(payload_encoded)
    
    log_it(session["client_ip"], session["client_header"], session["response_code"], size)
    
    connection.sendto(payload_encoded, client)
    
def unpack_header(header):
    response_txt = ""
    header_lines = header.split("\r\n")
    request = header_lines[0].split(" ")
    methode = request[0]
    file = request[1]
    httpv = request[2]

    print(header_lines[0])
    
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
    
    session["client_ip"] = client[0]
    session["client_header"] = header_lines[0]
    
    send_reply(methode, response_txt)

while True:
    connection ,client = s.accept()
    try:
        data = connection.recv(2048).decode()
        if data != "":
            unpack_header(data)
            connection.close()
    except:
        connection.close()
s.close()

import socket

PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))
s.listen(5)

def log_it(log):
    try:
        with open("log.txt", "a") as log_file:
            log_file.write(log + "\n")
    except:
        pass

def send_reply(response, body):
    if response == "404":
        header = "HTTP/1.1 404 NOT FOUND\r\n\r\n"

    elif response == "GET":
        header = "HTTP/1.1 200 OK\r\n"
        header += "Content-Type: text/html\r\n\r\n"

    payload = header + body
    connection.sendto(payload.encode(), client)

    print("send response to client")

def unpack_header(header):
    response_txt = ""
    header_lines = header.split("\r\n")
    request = header_lines[0].split(" ")
    methode = request[0]
    file = request[1]
    httpv = request[2]

    print("methode: " + methode)
    print("file: " + file)
    print("http v:" + httpv)

    log_it(f"Request: {methode}, file: {file}, client IP: {client[0]}")

    if methode == "GET":
        if file == "/":
            file = "/index.html"
        
        try:
            with open(file[1:]) as f:
                response_txt = f.read()
        except:
            methode = "404"

    log_it(f"Response: {methode}, file: {file}, client IP: {client[0]}")
    
    send_reply(methode, response_txt)

while True:
    connection , client = s.accept()
    data = connection.recv(2048).decode()
    if data != "":
        unpack_header(data)
        connection.close()
s.close()

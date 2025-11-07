import socket

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096).decode()
    return response

def upload_file(host, port, filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
    content_length = len(file_data)

    
    request = f"POST /upload HTTP/1.1\r\nHost: {host}\r\nContent-Length: {content_length}\r\n\r\n"
    request += file_data.decode('utf-8', errors='ignore')
    
    response = send_request(host, port, request)
    return response

def download_file(host, port, filename):
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    response = send_request(host, port, request)

    file_content = response.split('\r\n\r\n', 1)[1]
    with open("downloaded_" + filename, 'wb') as file:
        file.write(file_content.encode())


if __name__ == "__main__":
    host = "example.com"   
    port = 80

    print("Uploading 'example.txt' to server...")
    upload_response = upload_file(host, port, 'example.txt')
    print("Upload response:")
    print(upload_response)

    print("\nDownloading 'example.txt' from server...")
    download_file(host, port, 'example.txt')
    print("File downloaded as 'downloaded_example.txt'")
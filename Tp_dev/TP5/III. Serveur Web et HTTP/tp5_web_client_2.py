import requests

def send_get_request(url):
    response = requests.get(url)

    print(f"Response from {url}:")
    print(f"Status Code: {response.status_code}")
    print("Content:")
    print(response.text)

if __name__ == "__main__":
    server_url = 'https://www.ynov.com'
    send_get_request(server_url)

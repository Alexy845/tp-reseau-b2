import requests

def get_content(url):
    response = requests.get(url)
    return response.text

def write_content(content, file):
    with open(file, 'w') as f:
        f.write(content)
        print(f"Content written to {file} successfully.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = get_content(url)
    if content:
        write_content(content, '/tmp/web_page')
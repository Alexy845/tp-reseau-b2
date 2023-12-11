import requests
import os

def get_content(url):
    response = requests.get(url)
    return response.text

def write_content(content, file):
    with open(file, 'w') as f:
        f.write(content)
        print(f"Content written to {file} successfully.")

def process_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        urls = f.readlines()
        for url in urls:
            url = url.strip()  
            url = url.replace('https://', '')  
            file_name = url.replace('/', '_')
            content = get_content(url)
            if content:
                file_path = f"/tmp/web_{file_name}"
                write_content(content, file_path)

if __name__ == "__main__":
    import time
    start_time = time.time()

    urls_file = 'file_with_urls.txt'  # Remplacez par votre fichier d'URLs
    if not os.path.isfile(urls_file):
        print(f"File '{urls_file}' not found.")
        exit(1)

    process_urls_from_file(urls_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for synchronous script: {execution_time} seconds")
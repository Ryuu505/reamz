import os
import re
import requests

def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = url.split("/")[-1]
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Done: {filename} downloaded successfully.")
        else:
            print(f"Error: Failed to download {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

url = input("Masukkan URL: ")
folder = "reamz2"
create_folder_if_not_exists(folder)

try:
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        links = re.findall(r'href=[\'"]?([^\'" >]+\.png|\.jpg|\.jpeg)', content)
        if links:
            for link in links:
                full_url = url + link if link.startswith('/') else link
                download_file(full_url, folder)
        else:
            print("Tidak ada tautan dengan akhiran file PNG, JPG, atau JPEG.")
    else:
        print(f"Error: Failed to fetch URL ({response.status_code})")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

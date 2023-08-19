import os
import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import re

session = requests.Session()

def find_image_links_in_sitemap(url, keywords):
    response = session.get(url)
    content = response.content

    root = ET.fromstring(content)
    links = []
    count = 0
    for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        link = elem.text
        if any(keyword.lower() in link.lower() for keyword in keywords):
            links.append(link)
            count += 1
            if count == 200:
                break

    image_links = []
    for link in links:
        response = session.get(link)
        html_content = response.text

        img_regex = r'<img[^>]+src\s*=\s*["\']([^"\']+)["\'][^>]*>'
        img_matches = re.findall(img_regex, html_content)
        for img_match in img_matches:
            image_links.append(img_match)

    return image_links, count

def download_image(link, filepath):
    try:
        response = session.get(link, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"Terjadi kesalahan saat mengunduh gambar: {link}")
        print(e)
        return False


sitemap_url = input("Masukkan URL dan tambahkan /sitemap.xml di akhiran : ")
keywords_input = input("Masukkan keyword (pisahkan dengan koma jika lebih dari satu): ")
keywords = [keyword.strip() for keyword in keywords_input.split(",")]

image_links, count = find_image_links_in_sitemap(sitemap_url, keywords)

print(f"Total hasil yang ditemukan: {count}")


folder_name = "cuy"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


with ThreadPoolExecutor() as executor:
    futures = []
    for i, link in enumerate(image_links):
        filename = link.split("/")[-1]
        filepath = os.path.join(folder_name, filename)
        future = executor.submit(download_image, link, filepath)
        futures.append(future)

    for i, future in enumerate(futures):
        result = future.result()
        if result:
            message = f"Gambar {i+1}/{len(image_links)} berhasil diunduh dan disimpan"
            print(colored(message, "green"))

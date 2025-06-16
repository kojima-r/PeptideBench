import json
import os
import requests
from tqdm import tqdm

host="https://rdfportal.org/download/"

def download(url, filename):
    if "content-length" not in requests.head(url).headers:
        print("SKIP:", requests.head(url).headers)
        return
    file_size = int(requests.head(url).headers["content-length"])
    res = requests.get(url, stream=True)
    pbar = tqdm(total=file_size, unit="B", unit_scale=True)
    with open(filename, 'wb') as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)
            pbar.update(len(chunk))
        pbar.close()


target="https://api.app.peptipedia.cl/files/downloads/{}.fasta"
filename="activities.json"
obj=json.load(open(filename))
for el in obj['results']['data']['activities']:
    url=target.format(el)
    print(url)
    download(url,"data/"+el+".fasta")

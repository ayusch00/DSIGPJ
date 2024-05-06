import requests
import os
import gzip
import shutil

def download_file(url):
    local_filename = url.split('/')[-1]
    local_directory = "tmp"
    local_path = os.path.join(local_directory, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_path

def decompress_gz(local_path):
    output_path = "data/" + os.path.basename(local_path).replace(".gz", "")
    with gzip.open(local_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_path


# Main
url = input("Enter the URL of the file: ")
local_path = download_file(url)
decompress_gz(local_path)
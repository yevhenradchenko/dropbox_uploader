from os.path import isfile

import requests
import os
from time import sleep

from dropbox.exceptions import ApiError
from tqdm import tqdm
import dropbox

IGNORED_FILES = ['main.py']


def image_downloader():
    image_url = 'https://thispersondoesnotexist.com/image'

    for count in tqdm(range(110)):
        image_data = requests.get(image_url).content

        with open(f'image_{str(count).zfill(2)}.jpg', 'wb') as handler:
            handler.write(image_data)

        sleep(0.5)


def ignore(filename):
    filename_lower = filename.lower()

    return filename_lower in IGNORED_FILES


if __name__ == '__main__':
    image_downloader()

    local_dir = os.path.abspath('.')
    dbx_token = dropbox.Dropbox('p_EcLMnQMcAAAAAAAAAADZU38UTpLbhcrlgbFaMRgwKxGuDFwuNAV0wU-zplRNk6')

    for file_name in os.listdir(local_dir):

        if not isfile(file_name):
            continue

        if ignore(file_name):
            continue

        local_path = os.path.abspath(file_name)
        relative_path = os.path.relpath(local_path, local_dir)
        dropbox_path = os.path.join('/Apps/face_db_upload', relative_path)

        with open(local_path, 'rb') as f:
            try:
                dbx_token.files_upload(f.read(), dropbox_path)
            except ApiError:
                print(dropbox_path)

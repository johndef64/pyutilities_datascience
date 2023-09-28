import os
import requests

class Downloader:

    # git clone
    def git_clone(repo_url, save_dir = os.getcwd()):
        cmd = f'git clone {repo_url} {save_dir}'
        os.system(cmd)

    def git_clone_sub(repo_url,sub ,save_dir = os.getcwd()+'\\temp\\'):
        cmd = f'git clone {repo_url} {save_dir}'
        os.system(cmd)
        # specify original path and destination path
        original_path = save_dir + sub
        destination_path = os.path.join(os.getcwd(), sub)
        os.rename(original_path, destination_path)
        delete = f'rmdir /s /q  {save_dir}'
        os.system(delete)
        print(save_dir)

    # Simple Downloader
    def get_file(url, file_name, dir = os.getcwd()):
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            file_path = os.path.join(dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(content)
            print(f"File downloaded successfully. Saved as {file_name}")
        else:
            print("Unable to download the file.")

    # Download single GitHub file from repository
    def get_gitfile(url, flag='', dir = os.getcwd()):
        url = url.replace('blob','raw')
        response = requests.get(url)
        file_name = flag + url.rsplit('/',1)[1]
        file_path = os.path.join(dir, file_name)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully. Saved as {file_name}")
        else:
            print("Unable to download the file.")

    # Download and Exrtact zip file from Zenodo
    def get_and_extract_zenodo(file, dir = os.getcwd(), ext = '.zip'):
        url='https://zenodo.org/record/8205724/files/'+file+'.zip?download=1'
        zip_file_name = file+ext
        extracted_folder_name = dir
        # Download the ZIP file
        response = requests.get(url)
        if response.status_code == 200:
            # Extract the ZIP contents
            with io.BytesIO(response.content) as zip_buffer:
                with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                    zip_ref.extractall(extracted_folder_name)
            print(f"ZIP file '{zip_file_name}' extracted to '{extracted_folder_name}' successfully.")
        else:
            print("Failed to download the ZIP file.")
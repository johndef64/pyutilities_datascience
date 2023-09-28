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

    # Download single GitHub file from repository ()
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

import glob
import pandas as pd

class File:
    # Check files in folder (with extension)
    def display_file(ext, contains='', path=os.getcwd()):
        file_pattern = os.path.join(path, "*."+ext)
        files = glob.glob(file_pattern)
        files_name = []
        for file in files:
            file_name = os.path.basename(file)
            files_name.append(file_name)

        print('Available .'+ext+' files:')
        files_df = pd.Series(files_name)
        file = files_df[files_df.str.contains(contains)]
        print(file)

    def display_subfolders(folder_path=os.getcwd()):
        subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
        print("Subfolders in", folder_path, ":")
        for subfolder in subfolders:
            print(subfolder)

    def get_subfolders(folder_path=os.getcwd()):
        subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
        return subfolders

    def get_files(ext, contains='', path=os.getcwd()):
        file_pattern = os.path.join(path, "*."+ext)
        files = glob.glob(file_pattern)
        files_name = []
        for file in files:
            file_name = os.path.basename(file)
            files_name.append(file_name)
        filtered_file = [item for item in files_name if isinstance(item, str) and contains in item]
        return filtered_file

    def get_files_pd(ext, contains='', path=os.getcwd()):
        # Create a file path pattern to match 'ext' files
        file_pattern = os.path.join(path, "*."+ext)
        # Use glob to get a list of file paths matching the pattern
        files = glob.glob(file_pattern)
        files_name = []
        # Get the list of 'ext' files
        for file in files:
            file_name = os.path.basename(file)
            files_name.append(file_name)
        files_sr = pd.Series(files_name)
        filtered_file = files_sr[files_sr.str.contains(contains)]
        return pd.Series(filtered_file)

    def delete_file(filename, path=os.getcwd()):
        try:
            os.remove(os.path.join(path, filename))
            print(f"File {filename} deleted successfully.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except PermissionError:
            print(f"Permission denied.")
        except Exception as e:
            print(f"Unable to delete file {filename}. Error: {str(e)}")

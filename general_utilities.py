import os
import re
import ast
import importlib
import subprocess

def simple_bool(message):
    choose = input(message+" (y/n): ").lower()
    your_bool = choose in ["y", "yes","yea","sure"]
    return your_bool

def check_and_install_requirements(requirements):
    missing_requirements = []
    for module in requirements:
        try:
            # Check if the module is already installed
            importlib.import_module(module)
        except ImportError:
            missing_requirements.append(module)
    if len(missing_requirements) == 0:
        pass
    else:
        x = simple_bool(str(missing_requirements)+" are missing.\nWould you like to install them all?")
        if x:
            for module in missing_requirements:
                subprocess.check_call(["pip", "install", module])
                print(f"{module}' was installed correctly.")
        else:
            exit()


#================================================================================================
# Dowloaders

check_and_install_requirements(['gdown'])

import io
import requests
import zipfile
import gdown


# git clone
def git_clone(repo_url,
              save_dir = os.getcwd()):
    cmd = f'git clone {repo_url} {save_dir}'
    os.system(cmd)
    print('done')


def git_clone_sub(repo_url,
                  subfolder,
                  temp_dir = os.getcwd()+'\\temp\\'):
    cmd = f'git clone {repo_url} {temp_dir}'
    os.system(cmd)
    # specify original path and destination path
    original_path = temp_dir + subfolder
    destination_path = os.path.join(os.getcwd(), subfolder)
    os.rename(original_path, destination_path)
    delete = f'rmdir /s /q  {temp_dir}'
    os.system(delete)
    print('done')


# Simple Downloader
def get_file(url,
             file_name,
             dir = os.getcwd()):
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
def get_gitfile(url,
                flag='',
                dir = os.getcwd()):
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

def get_and_extract(file, dir = os.getcwd(), ext = '.zip'):
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


def get_gdown(url, output=None):
    """
    This function downloads a file from the internet using gdown.
    Args:
    url (str): The URL of the file you want to download.
    output (str, optional): The path where the downloaded file will be saved.
                            If not provided, the file will be saved in the current directory with its original name.
    """
    gdown.download(url, output, quiet = False)

def get_from_gdrive(gdrive_id, output):
    url_template = 'https://drive.google.com/uc?id={}'
    url = url_template.format(gdrive_id)

    gdown.download(url, output, quiet=False)

# Usage: download_from_gdrive('your Google Drive file ID', 'output file name')
# please replace 'your Google Drive file ID' and 'output file name' with real google drive id and local name for downloaded file.

# Download and Exrtact zip file from Zenodo
def get_and_extract_zenodo(file,
                           zenodoid = 8205724,
                           dir = os.getcwd(),
                           ext = '.zip'):
    url='https://zenodo.org/record/'+str(zenodoid)+'/files/'+file+'.zip?download=1'
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

#================================================================================================
# File
check_and_install_requirements(['pandas'])

import glob
import pandas as pd


# Check files in folder (with extension)
def file_display(ext,
                 contains='',
                 path=os.getcwd()):
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


def file_display_subfolders(folder_path=os.getcwd()):
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    print("Subfolders in", folder_path, ":")
    for subfolder in subfolders:
        print(subfolder)


def file_get_subfolders(folder_path=os.getcwd()):
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders


def file_get_files(ext,
                   contains='',
                   path=os.getcwd()):
    file_pattern = os.path.join(path, "*."+ext)
    files = glob.glob(file_pattern)
    files_name = []
    for file in files:
        file_name = os.path.basename(file)
        files_name.append(file_name)
    filtered_file = [item for item in files_name if isinstance(item, str) and contains in item]
    return filtered_file


def file_get_files_pd(ext, contains='',
                      path=os.getcwd()):
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


def file_delete(filename,
                path=os.getcwd()):
    try:
        os.remove(os.path.join(path, filename))
        print(f"File {filename} deleted successfully.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except PermissionError:
        print(f"Permission denied.")
    except Exception as e:
        print(f"Unable to delete file {filename}. Error: {str(e)}")

#================================================================================================
# Data Analysis

def pd_choose(my_list):
    i = int(input('choose index:\n'+str(pd.Series(my_list))))
    return my_list[i]


def pd_choose_col(my_df):
    i = int(input('choose column:\n'+str(pd.Series(my_df.columns))))
    return my_df.columns[i]


# Df merger
def pd_merge_base(df1, df2, column1, column2, how= ''):
    merged_df = pd.merge(df1, df2, left_on=column1, right_on=column2, how=how)
    return merged_df


def pd_merge_select(df1, df2, how= 'inner'):
    column1 = df1.columns[int(input(pd.Series(df1.columns)))]
    column2 = df2.columns[int(input(pd.Series(df2.columns)))]
    merged_df = pd.merge(df1, df2, left_on=column1, right_on=column2, how=how)
    return merged_df


def pd_merge_select_multi(df1, df2):
    how = pd_choose(['inner', 'outer','left', 'right','cross' ])
    column1 = df1.columns[int(input(pd.Series(df1.columns)))]
    column2 = df2.columns[int(input(pd.Series(df2.columns)))]
    merged_df = pd.merge(df1, df2, left_on=column1, right_on=column2, how=how)
    return merged_df


def pd_groupby_describe(df1):
    var = ['all','number','object','bool']
    include = pd_choose(var)
    column1 = df1.columns[int(input(pd.Series(df1.columns)))]
    df1_count = df1.groupby(column1).describe(include=include).dropna(axis=1,how='all').reset_index()
    return df1_count


def pd_groupby_describe_flat(df1):
    include = pd_choose(['all','number','object','bool'])
    column1 = df1.columns[int(input(pd.Series(df1.columns)))]
    df1_count = df1.groupby(column1).describe(include=include).dropna(axis=1,how='all').reset_index()
    df1_count.columns = df1_count.columns.to_flat_index()
    #pattern = r"([\w]+)_([\w]+)"
    list_of_strings = []
    for tuple in df1_count.columns:
        string = "_".join(tuple)
        #string = re.sub(r"\s+", "", string)
        list_of_strings.append(string)
    df1_count.columns = list_of_strings
    return df1_count


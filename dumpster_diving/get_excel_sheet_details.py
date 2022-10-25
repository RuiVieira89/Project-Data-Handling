
from django.conf import settings
import shutil
import zipfile
import xmltodict
import warnings
import os


def get_sheet_sheetName(file_path):
    # returns the sheets name and ID

    settings.configure()

    sheets = []
    file_name = os.path.splitext(os.path.split(file_path)[-1])[0]
    # Make a temporary directory with the file name
    directory_to_extract_to = os.path.join(settings.MEDIA_ROOT, file_name)
    try:
        os.mkdir(directory_to_extract_to)
    except os.path.isdir(directory_to_extract_to):
        warnings.warn("Folder already exists")
    except not os.path.isdir(directory_to_extract_to):
        warnings.warn("Could not create folder")

    # Extract the xlsx file as it is just a zip file
    # shutil.unpack_archive(file_name, directory_to_extract_to, 'xlsx')
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

    # Open the workbook.xml which is very light and only has meta data, get
    # sheets from it
    path_to_workbook = os.path.join(
        directory_to_extract_to, 'xl', 'workbook.xml')
    with open(path_to_workbook, 'r') as f:
        xml = f.read()
        dictionary = xmltodict.parse(xml)
        for sheet in dictionary['workbook']['sheets']['sheet']:
            sheet_details = {
                'id': sheet['@sheetId'],  # can be @sheetId for some versions
                'name': sheet['@name']  # can be @name
            }
            sheets.append(sheet_details)

    # Delete the extracted files directory
    # solve thouble with onedrive
    FLAG = True
    while FLAG:
        try:
            shutil.rmtree(directory_to_extract_to)
            FLAG = False
        except os.path.isdir(directory_to_extract_to):
            FLAG = True
            warnings.warn(
                "Waiting for One drive to allow the delete temporary files")
        except not os.path.isdir(directory_to_extract_to):
            FLAG = True  # already removed

    return sheets

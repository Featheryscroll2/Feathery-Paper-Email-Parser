import zipfile
import hashlib
import io
import virustotal_python
from exchangelib import FileAttachment
import base64
import json
import requests
import os
import pysftp

# FTP set up

with open("config.json", "r") as f:
    config = json.load(f)

# get the value for FTP server properties
if config['USE_FTP']:
    FTP_HOST = config['FTP_HOST']
    FTP_USER = config['FTP_USER']
    FTP_PASS = config['FTP_PASS']
    local_file_path = config['local_file_path']
    remote_file_path = config['remote_file_path']

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None


######

def upload_file_check_virus(attachment: FileAttachment, api: str, hash_str: str):
    # Create dictionary containing the file to send for multipart encoding upload
    try:
        files = {"file": (attachment.name, attachment.content)}
        with virustotal_python.Virustotal(api) as vtotal:
            vtotal.request("files", files=files, method="POST")
            params = {'apikey': api,
                      'resource': hash_str}
            url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
            json_response = url.json()
            positive = json_response.get('positives')
            total = json_response.get('total')
            if positive is not None and total is not None:
                result = f"{positive}/{total}"
            else:
                result = "N/A"
            return {
                "error": False,
                "msg": f"Virus total check successfully for this hash attachment {hash_str} with the score: {result}"
            }
    except Exception as e:
        print(f"Error occurred during virus check: {e}")
        return {
            "error": True,
            "msg": f"Virus total check failed for this hash attachment : {hash_str}"
        }


def send_hash_file_to_ftp_server(filename: str):
    try:
        with pysftp.Connection(host=FTP_HOST, username=FTP_USER, password=FTP_PASS, cnopts=cnopts) as sftp:
            sftp.cwd(remote_file_path)  # Switch to a remote directory
            sftp.listdir_attr()  # Obtain structure of the remote directory
            local_files = os.listdir(local_file_path)
            for file_name in local_files:
                if file_name == filename:
                    local_path = os.path.join(local_file_path, file_name)
                    remote_path = os.path.join(remote_file_path, file_name)
                    sftp.put(local_path, remote_path)
                    os.remove('attachments/' + filename)
                    break
        return {
            "error": False
        }
    except Exception as e:
        print("An error occurred:", e)
        return {
            "error": True,
            "msg": f"Sent {filename} to FPT server failed"
        }


# Create function to return the actual url
def hash_the_attachment(attachment: FileAttachment) -> str:
    # Decode the attachment content from base64
    content = base64.b64decode(attachment.content)
    hash_obj = hashlib.sha256(content)
    file_hash = hash_obj.hexdigest()
    return file_hash


# create function to zip and hash attachment
def zip_attachment(attachment: FileAttachment, hash_str: str):
    # Decode the attachment content from base64
    content = base64.b64decode(attachment.content)

    # # Create a memory buffer to write the file to
    file_buffer = io.BytesIO(content)

    # # Create a zip file
    zip_file = zipfile.ZipFile(file_buffer, 'w')

    # # Encrypt the contents of the zip file: this secret key can put to the config file
    zip_file.setpassword(config['zip_pass'].encode('utf-8'))  # make config

    # # Write the encrypted contents to the zip file
    zip_file.writestr(attachment.name, content)

    # # Close the zip file
    zip_file.close()

    # # Reset the file buffer position to the beginning
    file_buffer.seek(0)
    # # Write the encrypted zip file to disk
    with open('attachments/' + hash_str + '.zip', 'wb') as file:
        file.write(file_buffer.read())

    # send the zip hash file to the server
    file_buffer.close()

import json
import os


def write_json_file(log_file):
    # Check if the file exists
    if not os.path.isfile("email.json"):
        # If the file does not exist, create an empty list
        email_list = []
    else:
        # If the file exists, check if it is empty
        file_size = os.stat("email.json").st_size
        if file_size == 0:
            # If the file is empty, create an empty list
            email_list = []
        else:
            # If the file is not empty, read the existing data
            with open("email.json", "r") as infile:
                email_list = json.load(infile)

    # Add the new dictionary to the list
    email_list.append(log_file)
    log_object = json.dumps(email_list, indent=4)
    # Debug: print the email_list to see if it contains unexpected data

    # Convert the list to JSON format and write to the file
    with open("email.json", "w") as outfile:
        outfile.write(log_object)

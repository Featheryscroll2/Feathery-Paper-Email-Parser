import json
import requests

with open("config.json", "r") as f:
    config = json.load(f)


def create_servicenow_ticket(ticket_detail):
    hash_str = ''
    for item in ticket_detail["Hash"]:
        hash_str = hash_str + item + ' '
    link_str = ''
    for link in ticket_detail["Links"]:
        link_str = link_str + link + ' '
    domain_str = ''
    for domain in ticket_detail["Domains"]:
        domain_str = domain_str + domain + ' '
    ######################
    # Content Formatting #
    ######################
    data2 = ""
    if config['Subject'] != '':
        if ticket_detail["Subject"] != "":
            data2 = data2 + config['Subject'] + ": " + ticket_detail["Subject"] + ", "
        else:
            data2 = data2 + config['Subject'] + ": empty, "
    if config['Forwarded From'] != '' and ticket_detail["Forwarded From"] != '':
        data2 = data2 + config['Forwarded From'] + ": " + ticket_detail["Forwarded From"] + ","
    if config['From'] != '':
        data2 = data2 + config['From'] + ": " + ticket_detail["From"] + ", "
    if config['Date'] != '':
        data2 = data2 + config['Date'] + ": " + ticket_detail["Email sent on"] + ", "
    if config['message-id'] != '':
        data2 = data2 + config['message-id'] + ": " + ticket_detail["message-id"] + ", "
    if config['Hashs'] != '' and hash_str != "":
        data2 = data2 + config['Hashs'] + ": " + hash_str + ", "
    if config['Links'] != '' and link_str != "":
        data2 = data2 + config['Links'] + ": " + link_str + ", "
    if config['Domains'] != '' and domain_str != "":
        data2 = data2 + config['Domains'] + ": " + domain_str + ", "
    if config['Threatsim'] != '':
        data2 = data2 + config['Threatsim'] + ": " + str(ticket_detail["Threatsim"])

    ###################
    # ServiceNow Post #
    ###################
    try:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = "{'description':'" "Payload: " + data2 + \
               "','assignment_group':'2','urgency':'2','impact':'2'}"
        response = requests.post(config["SNInstance"], auth=(config["SNUsername"],
                                                             config["SNPassword"]), headers=headers, data=data)
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            return {
                "error": False,
                "msg": "Incident created successfully"
            }
        elif response.status_code == 400:
            return {
                "error": True,
                "msg": "Bad Request! Sent from ServiceNow"
            }
        elif response.status_code == 401:
            return {
                "error": True,
                "msg": "Unauthorized Access! Sent from ServiceNow"
            }
        else:
            return {
                "error": True,
                "msg": "An error occurred! Sent from ServiceNow"
            }
    except Exception as e:
        return {
            "error": True,
            "msg": f"An error occurred while creating incident! Sent from ServiceNow: {e}"
        }

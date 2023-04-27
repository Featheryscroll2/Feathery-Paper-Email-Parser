from exchangelib import Credentials, Account, FileAttachment
import json
from bs4 import BeautifulSoup
import attachmentFucntions
import syslogFunction
import machine_learning.apply
# This process_text is used for machine learning
from machine_learning.apply import process_text
import datetime
import forwardFunction
import usefulFunction
import linkFunctions
import writeJsonFileFunction
import servicenowFunctions
###############
# reads a JSON-formatted configuration file named "config.json" and loads its contents intoconfig.
with open("config.json", "r") as f:
    config = json.load(f)

###############
# Login to email inbox using email and password
###############
try:
    email = str(config["Email Address"])
    password = str(config["Password"])
    credentials = Credentials(email, password)
    account = Account(email, credentials=credentials, autodiscover=True)
    # Main information and variable declarations
    for item in account.inbox.all().order_by('-datetime_received')[:1]:
        # Define initial values for email properties
        body_unencoded = item.text_body
        body = body_unencoded.encode('ascii', 'ignore').decode()
        threatsim = False
        # Check if the email was forwarded
        forwarded_from = forwardFunction.find_forward_email(str(body))
        if "threatsim" in item.message_id:
            threatsim = True
        ######################
        # Define initial value for email properties #
        ######################
        email_data = {
            "-------------------------------": '',
            "System time of this run": usefulFunction.get_local_time(),
            "Email type": [],
            "ServiceNow connection status": '',
            "Subject": item.subject,
            "Forwarded From": forwardFunction.find_forward_email(str(body)),
            "From": str(item.sender.email_address),
            "Email sent on": str(item.datetime_received),
            "message-id": item.message_id,
            "Body": body,
            "Hash": [],
            "Links": [],
            "Domains": [],
            "Threatsim": threatsim,
            "Machine learning model predicts email": "N/A",
            "Total errors": 0,
            "Error detail": []
        }

        #######################
        # Attachment Handling #
        #######################

        if item.attachments:
            email_data["Email type"].append("Attachment")  # checks for attachments in email
            virus_total_status = []
            virus_error = 0
            check_ftp_error = 0
            for attachment in item.attachments:  # goes through each attachment
                if isinstance(attachment, FileAttachment):
                    hash_str = attachmentFucntions.hash_the_attachment(attachment)
                    email_data["Hash"].append(hash_str)
                    attachmentFucntions.zip_attachment(attachment, hash_str)
                    virus_result = attachmentFucntions.upload_file_check_virus(attachment,
                                                                               config["Virus_total_api"], hash_str)
                    if virus_result["error"]:
                        virus_total_status.append(virus_result["msg"])
                        virus_error += 1
                    else:
                        virus_total_status.append(virus_result["msg"])
                    # use FTP to send zip file to server
                    if config["USE_FTP"]:
                        file_name = hash_str + ".zip"
                        ftp_result = attachmentFucntions.send_hash_file_to_ftp_server(file_name)
                        if ftp_result["error"]:
                            check_ftp_error += 1
            if virus_error > 0:
                email_data["Total errors"] += 1
                email_data["Error detail"].append("Failed to send file to virus total to check")
            if check_ftp_error > 0:
                email_data["Total errors"] += 1
                email_data["Error detail"].append("Failed when using FTP to send zip file to server")
            email_data["Virus total status"] = virus_total_status
        #################
        # Link Handling #
        #################
        html_body = item.body
        soup = BeautifulSoup(html_body, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        if len(links) > 0:
            link_result = linkFunctions.get_url_domain(links)
            email_data["Links"] = link_result["links"]
            email_data["Domains"] = link_result["domains"]
            if len(link_result["links"]) > 0:
                email_data["Email type"].append("Link")
            if len(link_result["errors"]) > 0:
                email_data["Total errors"] += 1
                email_data["Error detail"].append("Failed when get encoded link from Proof Point")

        ######################
        # Check if email is spam or not #
        ######################
        email_data["Email type"].append("Text")
        # only check spam if the email contain text or url
        if email_data["Email type"][0] == "Text" or email_data["Email type"][0] == "Link":
            spam = machine_learning.apply.check_spam(body)
            if spam == 1:
                email_data["Machine learning model predicts email"] = "Spam"
            else:
                email_data["Machine learning model predicts email"] = "Not spam"
        #################
        # Create incident in ServiceNow #
        #################
        if config["USE_SERVICE"]:
            service_result = servicenowFunctions.create_servicenow_ticket(email_data)
            if service_result["error"]:
                email_data["Total errors"] += 1
                email_data["ServiceNow connection status"] = service_result["msg"]
                email_data["Error detail"].append("Failed to create incident from ServiceNow")
            else:
                email_data["ServiceNow connection status"] = service_result["msg"]
        #################
        # Check warning email
        #################
        warning_result = usefulFunction.check_warning_email(email_data)
        email_data["Warning count"] = warning_result["warning_count"]
        email_data["Warning detail"] = warning_result["warning_detail"]
        #################
        # Send log object to syslog server
        #################
        log_object = json.dumps(email_data, indent=4)
        if config["Syslog server"]:
            syslog_result = syslogFunction.sent_syslog(log_object)
            if syslog_result["error"]:
                email_data["Total errors"] += 1
                email_data["Error detail"].append(syslog_result["msg"])
        #################
        # write email detail to log txt file
        #################
        with open('log.txt', 'a', encoding='utf-8') as txt_file:
            txt_file.write(log_object)
            txt_file.write("\n")
        #################
        # write email detail to Json file
        #################
        if config["makeJSON"]:
            writeJsonFileFunction.write_json_file(email_data)
        #######################
        # Delete Parsed Email #
        #######################
        if config["deleteEmails"]:
            item.move(account.trash)
except Exception as e:
    with open('log.txt', 'a', encoding='utf-8') as txt_file:
        txt_file.write(json.dumps({
            "Error": f"System run failed with msg: {e}",
            "Date": str(datetime.datetime.now())
        }, indent=4))
        txt_file.write("\n")
    print("System failed.")

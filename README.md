##############################################################
# The Feathery Pen Email Parser                              #
##############################################################

**Disclaimer Since this program uses exchangelib, the best results occur when the program reads from an outlook account**

**Description**: The program links to a specified email address and converts email messages into a universal data 
object that can be read by 3rd party softwares such as ServiceNow to create organized tickets.
The data sent through includes all of the important email data such as subject, email address who sent 
the email, any attachments the email included, and more described below. Along with creating 
data objects, the program also allows for spam predictions by allowing for a machine learning
model to be created using a user specified data set, as well as VirusTotal scans for all attachments
sent in the email. The program is written in Python 3.11 and uses exchangelib to connect to email and parse 
its data

**Files Included**
    emailFunctions.py<br/>
    exchangelibtest.py<br/>
    log.txt<br/>
    config.json<br/>
    requirement.txt<br/>
    syslog_func.py<br/>

**Full Features**
    Read and parse emails into universal data objects<br/>
    Ability to alter the data topics put in to the data objects<br/>
    Send Data Objects to serviceNow<br/>
    Send email attachments thorugh an SFTP server<br/>
    scan email attachments through VirusTotal and recieve outcome<br/>
    Create a machine learning model to predict whether an email is spam or not based on text<br/>


**The list of Data topics the program can output in data object**
    Email subject<br/>
    Person who forwarded email<br/>
    Person who sent email<br/>
    Body text<br/>
    Date sent<br/>
    Message-id<br/>
    Any attachment hashes included in email<br/>
    Any links that are included in email<br/>
    The domains attached to any links in the email<br/>


**Config File Variables**
    Email Address: This variable holds the main email address that the program will read emails from<br/>
    Password: This holds the password for the main email<br/>
    sendToSn: When true, the program will send the data object to ServiceNow, when false it will not<br/>
    SNInstance: Holds the ServiceNow instance the program will send the data object to<br/>
    SNUsername: Holds the username used to sign into the ServiceNow instance<br/>
    SNPassword: Holds the password used to sign into the serviceNow instance  
    client_id:  
    client_secret:<br/>
    access_token_url:<br/>
    authorize_url:<br/>
    redirect_url:<br/>
    SFTPServer: holds the SFTP URL that the program will send the attachements accross<br/>
    SFTPUsername: holds the SFTP username for the SFTP server <br/>
    SFTPPassword: holds the password for the SFTP server<br/>
    makeLogFile: when true, email information, errors, and more will be added to a log file <br/>
    deleteEmails: when true, program will send emails the program has parsed into the trash folder<br/>
    zip_pass: Hold sthe password needed to zip up attachments<br/>
    Syslog server:<br/>
    Host: <br/>
    Port:<br/>
    FTP_HOST:<br/>
    FTP_USER:<br/>
    FTP_PASS:<br/>
    local_file_path:<br/>
    remote_file_path:<br/>
    Subject: Holds the name of the topic that will hold the subject of the email (put "" if you want to exclude all together)<br/>
    Forwarded From: Holds the name of the topic that will hold the email address that forwarded the message (put "" if you want to exclude all together)<br/>
    From: Holds the name of the topic that will hold the email address who sent the original message (put "" if you want to exclude all together)<br/>
    Date: Holds the name of the topic that will hold the date the email was sent to main email (put "" if you want to exclude all together)<br/>
    message-id: Holds the name of the topic that will hold the message-id of the email (put "" if you want to exclude all together)<br/>
    Body: Holds the name of the topic that will hold the body text of the email (put "" if you want to exclude all together)<br/>
    Hashs: Holds the name of the topic that will hold the list of attachment hashes included in the email (put "" if you want to exclude all together)<br/>
    Links: Holds the name of the topic that will hold the list of links that were included in the email (put "" if you want to exclude all together)<br/>
    domains: Holds the name of the topic that will hold the list of domains that the links in the email included (put "" if you want to exclude all together)<br/>
    threatsim: Holds the name of the topic that will hold whether or not the the email was a simulation or not (put "" if you want to exclude all together)<br/>


**Machine Learning**


**SFTP transfer**

**Starting Instructions**

1. Go through the config file and modify only the the information to the right of the colons the way you want your program to run including the email
information, servicenow information, any debugging variables, etc. <br/>
2. Run the program and look for results in either the log file or the 3rd party software that is connected<br/>
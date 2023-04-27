import time
###########################
# Check warning
###########################


def check_warning_email(email_detail):
    warning_count = 0
    warning_detail = []
    if email_detail["Subject"] == "":  # Catches blank subject field in email
        warning_detail.append("Email subject line left blank")
        warning_count += 1
    if not email_detail["Subject"].isascii():  # Confirms only ASCII characters
        warning_detail.append("Email subject contains non-ASCII characters")
        warning_count += 1
    if email_detail["From"] == "":  # Catches blank subject field in email
        warning_detail.append("Email sender address (from:) left blank")
        warning_count += 1
    if not email_detail["From"].isascii():
        warning_detail.append("Email sender address contains non-ASCII characters")
        warning_count += 1
    if email_detail["Body"] == "":  # Catches blank body field in email
        warning_detail.append("Email body field left blank")
        warning_count += 1
    if not email_detail["Body"].isascii():
        warning_detail.append("Email body contains non-ASCII characters")
        warning_count += 1
    return {
        "warning_count": warning_count,
        "warning_detail": warning_detail
    }


def get_local_time():
    system_time = time.localtime()
    time_tag = time.strftime("%Y-%m-%d %H:%M:%S", system_time)
    ms = time.time() * 1000.0
    return time_tag + ":" + str(ms)

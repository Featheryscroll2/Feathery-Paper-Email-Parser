# Please note that this is only formatted to search for emails sent
# through the Outlook system. It may produce unexpected outputs
# if used on other email systems.
def find_forward_email(fw_original: str):
    address_start = "From: "
    address_start2 = "<"
    address_start3 = "<mailto:"
    address_end = ">"
    out1 = ""
    out2 = ""
    forwarded_from = ""
    try:
        if address_start in fw_original:
            start_index = fw_original.index(address_start) + len(address_start)
            out1 = fw_original[start_index:]
    except ValueError:
        print("Error: addressStart not found")
    try:
        if address_end in out1:
            end_index = out1.index(address_end)
            out2 = out1[:end_index]
    except ValueError:
        print("Error: addressEnd not found")
    try:
        if address_start2 or address_start3 in out2:
            if address_start2 in out2:
                start_index = out2.index(address_start2) + len(address_start2)
                forwarded_from = out2[start_index:]
            if address_start3 in out2:
                start_index = out2.index(address_start3) + len(address_start3)
                forwarded_from = out2[start_index:]
    except ValueError:
        print("Error: addressStart not found")
    return forwarded_from

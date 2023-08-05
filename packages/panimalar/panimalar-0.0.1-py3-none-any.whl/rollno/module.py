import regex



def isvalid(rollno):
    """
    Check if rollno is valid (eg. 2021PECCB001)
    Returns True if valid, False otherwise
    """

    # Regex for rollno
    regex_rollno = r'^20[1-3]{1}[0-9]{1}(PEC)[A-Z]{2}[0-9]{3}$'

    # Check if rollno is valid
    if regex.match(regex_rollno, rollno.strip().upper()):
        return True
    else:
        return False



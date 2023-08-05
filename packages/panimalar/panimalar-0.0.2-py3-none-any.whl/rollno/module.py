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


def getdeptcode(rollno):
    """
    Get department code from rollno
    Returns department code if valid, None otherwise
    """

    # Check if rollno is valid
    if isvalid(rollno):
        # Get department code
        department_code=rollno[5:7]

        return department_code
    else:
        return None




def getdept(rollno):
    """
    Get department from rollno
    Returns department if valid, None otherwise
    """

    # Check if rollno is valid
    if isvalid(rollno):
        departments = {
            'CB': 'Computer Science and Business Systems',
            'CS': 'Computer Science and Engineering',
            'IT': 'Information Technology',
            'EC': 'Electronics and Communication Engineering',
            'EE': 'Electrical and Electronics Engineering',
            'CE': 'Computer Science and Engineering',
            'CC': 'Computer Science and Communication Engineering',
            'ME': 'Mechanical Engineering',
            'AD': 'Artificial Intelligence and Data Science'
        }

        # Get department code
        department_code=getdeptcode(rollno)

        # Get department name and return
        department=  departments[department_code]
        return department
    else:
        return None
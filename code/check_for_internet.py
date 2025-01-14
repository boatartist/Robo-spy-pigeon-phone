import subprocess
def check_for_internet():
    try:
        subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])
        return True
    except subprocess.CalledProcessError:
        return False

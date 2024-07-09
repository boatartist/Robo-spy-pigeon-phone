def check_for_internet():
    try:
        import requests
        req = requests.get('https://github.com/boatartist')
        return True
    except:
        return False

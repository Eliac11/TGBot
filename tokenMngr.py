import importlib
def getToken():
    try:
        token = open("token.txt").read().replace("\n", "")
        return token
    except:
        print("---Text file with token not found")

    print("search for an encrypted library with a token ")

    try:
        token = importlib.import_module("telebottoken").KEY
        return token
    except:
        print("---Text encrypted library with token not found")

    print("Launch is not possible without a token")
    raise Exception("token not found")
    quit()

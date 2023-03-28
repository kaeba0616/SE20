import os


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


for x in range(0, 10):
    createFolder(f"./unogame/resource/images/card/normalMode/{x}")

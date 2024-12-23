import os


def createPathIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

"""
Function Loader
"""
import sys
from rias.compimg import *
from rias.compvideo import *
from rias.imgloader import main as imgloadermain


# Loader
def loader(content) -> None:
    if content == None:
        print("No Module Loaded")
        sys.exit(0)
    print(f"connect loader.\n content -> {loader}\n\n")
    if content == "compimg" or content == "compimage":
        compimg()
    elif content == "compvid" or content == "compvideo":
        compvideo()
    elif content == "imgloader" or content == "getimg":
        imgloadermain()

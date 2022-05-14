#!/usr/bin/python
import json
import os
import sys
# TODO switch to urllib3
import urllib.request

from colorama import Fore, Style

DIR = os.path.expanduser('~') + "/.flexicon"
PACKAGES = DIR + "/packages"
TEXMF = os.path.expanduser('~') + "/texmf/tex/latex/"


def package_pretty_print(package: dict) -> None:
    print(Fore.GREEN + package['name'] + ': ' + Style.RESET_ALL + package['caption'])


def usage(message=None) -> None:
    if message:
        print(message)
    print("flexicon — a simple TeX packages manager\nUsage: flexicon [command] (package)\nCommands:\n\tupdate\t\tUpdate packages database\n\tsearch\t\tPrimitive packages search\n\tinstall\t\tInstall a package")


def update() -> None:
    os.makedirs(DIR, exist_ok=True)
    with urllib.request.urlopen("https://ctan.org/json/2.0/packages") as packages:
        if packages.code == 200:
            with open(PACKAGES, "w") as f:
                f.write(packages.read().decode('utf-8'))
        else:
            raise Exception("Cannot reach packages database. Are you sure you have internet connection available?")
    print("Done.")


def search(query: str) -> None:
    try:
        with open(PACKAGES) as f:
            db = json.load(f)
            for package in db:
                if package['name'].count(query) > 0 or package['caption'].count(query) > 0:
                    package_pretty_print(package)
    except:
        print("Cannot read local database: have you run 'flexicon update' beforehand?")


def install(query: str) -> None:
    os.makedirs(TEXMF, exist_ok=True)
    print("Retrieving package " + query + "...")
    with urllib.request.urlopen("https://www.ctan.org/json/2.0/pkg/" + query) as f:
        if f.code != 200:
            raise Exception("Cannot get package " + query)
        metadata = json.loads(f.read().decode('utf-8'))
        with urllib.request.urlopen(f"https://mirrors.ctan.org{metadata['ctan']['path']}.zip") as package:
            tmp = "." + query + ".zip"
            with open(TEXMF + tmp, 'wb') as f:
                f.write(package.read())
        path = os.curdir
        os.chdir(TEXMF)
        os.system(f"unzip {tmp} > /dev/null")
        print("Installing " + query)
        os.chdir(TEXMF + query)
        if os.path.exists(query + ".ins"):
            os.system("latex " + query + ".ins")

        os.chdir(path)
        os.remove(TEXMF + tmp)
    print(Fore.GREEN + "Installed: " + Style.RESET_ALL + query)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
    elif sys.argv[1] not in ["install", "search", "update"]:
        usage("Unknown command: " + sys.argv[1])
    else:
        cmd = sys.argv[1]
        arg = None
        if len(sys.argv) > 2:
            arg = sys.argv[2]
        # No switches?
        # ⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
        # ⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
        # ⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
        # ⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
        # ⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
        # ⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
        # ⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        # ⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        if cmd == "search":
            search(arg)
        elif cmd == "install":
            install(arg)
        elif cmd == "update":
            update()

# change USR_DIR to the location of your user installation
USR_DIR = "/home/timy/.local" 
# change SYS_DIR to your system installation (don't need to be precise, as long as distinguishable from USR_DIR)
SYS_DIR = "/usr/lib/python3"

import os
import json

def executeCommand(command: str) -> str:
    stream = os.popen(command) # open a pip from the command line
    result = stream.read() # read from the stream
    return result.split("\n")

def parsePackageInfoFromPip(packageName: str) -> tuple:
    """ Parse the package information by running "pip show".
    """
    lines = executeCommand(f"python3 -m pip show {packageName}")
    name: str
    location: str
    requires: list[str] = []
    required: list[str] = []
    for iLine, line in enumerate(lines):
        l = line.split()
        if len(l) > 0:
            if l[0] == "Name:" and iLine == 0:
                name = l[1]
            elif l[0] == "Location:":
                location = l[1]
            elif l[0] == "Requires:" and len(l) > 1:
                requires = [pkg.strip(",") for pkg in l[1:]]
            elif l[0] == "Required-by:" and len(l) > 1:
                required = [pkg.strip(",") for pkg in l[1:]]
    return name, location, requires, required

def createPackagesDict(packageNames: list[str]) -> dict:
    """ Create a dictionary of package information for the given list of package names.
    """
    packages = dict()
    for packageName in packageNames:
        name, location, requires, required = parsePackageInfoFromPip(packageName)
        packages[name] = dict()
        packages[name]["location"] = location
        packages[name]["requires"] = requires
        packages[name]["required"] = required
        print(f"Package '{name}' completed")
    return packages

def rebuildIndex(jsonFileName="pip_packages.json"):
    """ Create a JSON file that stores details of all Python packages installed 
    in the current system, including system default installations (SYS_DIR) and
    user's installations (USR_DIR).
    """

    # retrieve installed packages
    lines = executeCommand("python3 -m pip list")

    # store package names in a list
    packageNames: list[str] = []
    for line in lines[2:-1]:
        items = line.split()
        packageNames.append(items[0])

    # retrieve details of packages, storing them in a dict
    packages = createPackagesDict(packageNames)

    # save the dict as a JSON file
    with open(jsonFileName, "w") as file:
        json.dump(packages, file, sort_keys=True, indent=4)

def upgradePackages():
    """ Upgrade outdated packages by running "pip install XXX --upgrade".
    Upgrade only user's installations, keeping system packages intact.
    """
    # load package details from database
    packages: dict[str, dict] = dict()
    with open("pip_packages.json", "r") as file:
        packages = json.load(file)

    # retrieved outdated packages
    lines = executeCommand("python3 -m pip list --outdated")

    # check each outdated package
    for line in lines[2:-1]:
        items = line.split()
        name = items[0]
        oldVersion = items[1]
        newVersion = items[2]
        # if the package is managed by user
        if packages[name]["location"].find(USR_DIR) >= 0:
            print("-"*40)
            print(f"Upgrading {name}...")
            results = executeCommand(f"python3 -m pip install {name} --upgrade")


def showUpgradablePackages():
    """ Show outdated packages by running "pip list XXX --outdated".
    Show only user's installations, keeping system packages intact.
    """

    # load package details from database
    packages: dict[str, dict] = dict()
    with open("pip_packages.json", "r") as file:
        packages = json.load(file)

    # retrieved outdated packages
    lines = executeCommand("python3 -m pip list --outdated")

    # check each outdated package
    count: int = 0
    for line in lines[2:-1]:
        items = line.split()
        name = items[0]
        oldVersion = items[1]
        newVersion = items[2]
        # if the package is managed by user
        if packages[name]["location"].find(USR_DIR) >= 0:
            print("-"*40)
            print(f"{name}\t\t{oldVersion}->{newVersion}")
            count += 1
    if count == 0:
        print("Python packages are up to date. No user installation needs upgrade.")

def createGraphvizOfPackageDependency(dotFileName="graph_test.dot"):
    """ Using Graphviz, generate a graph illustrating dependency relations 
    of all installed Python packages. System installations are depicted by 
    red nodes, while user installations are depicted by blue nodes. 
    """
    packages: dict[str, dict] = dict()
    with open("pip_packages.json", "r") as file:
        packages = json.load(file)

    dotString: str = "digraph G {\n"
    dotString += "\tlayout=dot\n"
    dotString += "\tranksep=10.0\n"
    dotString += "\tnode [ style = filled ];\n"

    def normalise(s: str):
        return '"' + s.replace("-", "_").lower() + '"'

    for k, v in packages.items():
        src = normalise(k)
        color: str = "gray"
        if v["location"].find(USR_DIR) >= 0:
            color = "cyan"
        elif v["location"].find(SYS_DIR) >= 0:
            color = "lightpink"

        dotString += f"\t{src} [color={color}]\n"
        if len(v["requires"]) > 0:
            for i in v["requires"]:
                des = normalise(i)
                dotString += f"\t{src}->{des}\n"
        
    dotString += "}"

    with open(dotFileName, "w") as file:
        file.write(dotString)
    imageFileName = f"{dotFileName.split('.')[0]}.svg"
    os.system(f"dot {dotFileName} -Tsvg > {imageFileName}")
    print(f"Illustration of package dependencies is generated. View file '{imageFileName}'.")


if __name__ == "__main__":
    # Step 1: Rebuild the index (COMPULSORY. You need to run this for the FIRST time, or after you installed/uninstall packages)
    # rebuildIndex()

    # Step 2: Generate image of package dependency (optional, if you wish to see the graph)
    createGraphvizOfPackageDependency()

    # Step 3: Show upgradable packages installed in user's directory (optional, if you want to view upgradable packages)
    # showUpgradablePackages()

    # Step 4: Show upgradable packages installed in user's directory (COMPULSORY if you want to do the actual upgrade!)
    # upgradePackages()

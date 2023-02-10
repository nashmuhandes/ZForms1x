import os
import shutil
from distutils.dir_util import copy_tree

zformsFiles = ["BaseMenu.zsc", "BoundingBox.zsc", "BoxTextures.zsc", "Button.zsc", "Element.zsc",
               "Frame.zsc", "Handler.zsc", "Image.zsc", "Label.zsc", "Include.zsc", "UiEvent.zsc",
               "BoxImage.zsc", ]

def main():
    while True:
        try:
            prefixUserPart = input("Input class prefix: ")
            prefixUserPart.encode("ascii")
            if prefixUserPart.lower() in ["gutawer", "zforms", "zf", "menu"]:
                print("Prefix too generic. Please choose a prefix unique to your mod.")
            elif len(prefixUserPart) in [0, 1]:
                print("Prefix too short. Prefix must be at least 2 chars.")
            else:
                break
        except UnicodeError:
            print("Prefix should contain only ASCII characters.")


    while True:
        underscores = input(f"Use underscores in class names (e.g. {prefixUserPart}_ZF_Example or {prefixUserPart}ZFExample)? ")
        if underscores.lower() in ["y", "yes"]:
            prefixUserPart += "_"
            prefix = prefixUserPart + "ZF_"
            break
        elif underscores.lower() in ["n", "no"]:
            prefix = prefixUserPart + "ZF"
            break
        else:
            print("Invalid input (please enter \"yes\" or \"no\").")

    newPathName = ""
    while True:
        newPathName = input("Input new path name: ")
        if os.path.isabs(newPathName):
            print("Only relative paths are accepted.")
        elif newPathName.lower() == "zforms":
            print("Can't override ZForms folder.")
        elif os.path.exists("Generated/" + newPathName):
            confirm = input(newPathName + " already exists. OK to overwrite? (Y/N) ")
            if confirm.lower() == "y":
                shutil.rmtree("Generated/" + newPathName)
                break
        else:
            break

    os.makedirs("Generated/" + newPathName)
    copy_tree("ZForms", "Generated/" + newPathName + "/" + prefixUserPart + "ZForms")
    shutil.copyfile("LICENSE.md", "Generated/" + newPathName + "/" + prefixUserPart + "ZForms/LICENSE.md")

    replacements = {"####": prefix, "##PATH##": prefixUserPart + "ZForms"}

    for n in zformsFiles:
        lines = []
        with open("Generated/" + newPathName + "/" + prefixUserPart + "ZForms/" + n) as infile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                lines.append(line)
        with open("Generated/" + newPathName + "/" + prefixUserPart + "ZForms/" + n, "w") as outfile:
            for line in lines:
                outfile.write(line)

if __name__ == "__main__":
    main()

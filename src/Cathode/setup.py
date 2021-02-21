
import setuptools
import shutil
import sys

version = "0.1"

#reads readme
with open("../../README.md",'r') as rdme:
    readme=rdme.read()

print("Installing: Cathode")
print("Copying ANCA_Connect.py")

shutil.copy2("../ANCA_Connect.py","./ANCA_Connect.py")
setuptools.setup(
        name='PWS-Cathode',
        version=version,
        description="PWS Robot internal code",
        packages=setuptools.find_packages(),
        long_description_content_type="text/markdown",
        )

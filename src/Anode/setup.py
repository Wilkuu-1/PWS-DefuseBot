
import setuptools
import shutil
import sys

version = "0.1"
choice = 'c' # 'a' for anode 'c for cathode'


#reads readme
with open("../../README.md",'r') as rdme:
    readme=rdme.read()

print(f"Installing: ")
print(f"Copying ANCA_Connect.py to: src/Anode/")

shutil.copy2("../ANCA_Connect.py","./ANCA_Connect.py")

setuptools.setup(
        name='PWS-Anode',
        version=version,
        description="PWS Robot remote controller",
        packages=setuptools.find_packages(),
        long_description_content_type="text/markdown",
        )

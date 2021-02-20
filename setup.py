import setuptools


version = "0.1"

#reads readme
with open("README.md",'r') as rdme:
    readme=rdme.read()

#asks which package to install
print("## PWS-DefuseBot building tool ##\n## choose software to compile:\n(A)node: controller side\n (C)athode: robot side")
choice = input().lower()[0]
progs ={'a':'src/Anode',
        'c':'src/Cathode'}
names={'a':'PWS-Anode',
        'c':'PWS-Cathode'}
desc={'a':"PWS Robot remote controller",
        'c':"PWS Robot internal code"}


print(f"Installing: {names.get(choice)}")
setuptools.setup(
        name=names.get(choice),
        version=version,
        description=desc.get(choice),
        package_dir={'':progs.get(choice)},
        packages=setuptools.find_packages(where=progs.get(choice)),
        long_description_content_type="text/markdown",
        )

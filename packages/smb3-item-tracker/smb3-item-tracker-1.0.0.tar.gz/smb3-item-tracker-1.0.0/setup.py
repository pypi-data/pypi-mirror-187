from setuptools import setup, find_packages

setup(
    name="smb3-item-tracker",
    version="1.0.0",
    description=("UI to handle tracking inventory in SMB3"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="smb3-item-tracker",
    author="Jon Robison",
    author_email="narfman0@blastedstudios.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[],
)

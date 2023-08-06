from setuptools import setup
with open("README.md","r") as fh:
    long_description=fh.read()
setup(
    name='Topsis_Mohit_102197021',
    version='0.0.1',
    description='multiple criteria decision making using topsis',
    py_modules=["topsis"],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas ~=1.5.2",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    author="Mohit",
    author_email="singlamohit444@gmail.com",
)
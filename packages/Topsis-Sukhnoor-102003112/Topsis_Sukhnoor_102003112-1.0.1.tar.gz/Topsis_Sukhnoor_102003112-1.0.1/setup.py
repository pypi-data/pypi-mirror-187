import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Sukhnoor_102003112",
    version="1.0.1",
    description="This is a Python library created for handling problems related to Multiple Criteria Decision Making(MCDM)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sukhnoor21/Topsis-Sukhnoor_102003112",
    author="Sukhnoor Kaur",
    author_email="sukhnoorkaur21@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis_Sukhnoor_102003112"],
    include_package_data=True,
    install_requires='pandas'
                   'tabulate',
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Sukhnoor_102003112.topsis:main",
        ]
    },
)
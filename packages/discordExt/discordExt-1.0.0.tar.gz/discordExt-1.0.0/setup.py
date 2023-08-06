from setuptools import setup
import os

# recursively find folders
def find_packages(path):
    packages = []
    for root, dirs, files in os.walk(path):
        if "__init__.py" in files:
            packages.append(root.replace("/", "."))
    return packages


setup(
    name="discordExt",
    version="1.0.0",
    author="Zackary W",
    description="extended utilities for discord.py",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/ZackaryW/discordPyExt",
    packages=find_packages("discordExt") + ["discordExt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        #alpha
        "Development Status :: 3 - Alpha",
        # for devs
        "Intended Audience :: Developers",
    ],
    #requires
    python_requires='>=3.6',
    install_requires=[
        "discord",
        "pydantic",
    ],
    extras_require={
        "test" : [
            "pdoc"
        ]
    },
    #entry points
    entry_points={
        "console_scripts": [
        ]
    },
)

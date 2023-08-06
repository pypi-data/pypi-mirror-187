import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Tsong",
    version = "0.0.1",
    author = "K4r4b0_M0kg0th0",
    author_email = "Mojurarecords@gmail.com",
    description = "simple program that allows you to play music on a linux terminal",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/K4r4b0M0kg0th0/Tsong",
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    install_requires=['pygame', 'mutagen'],
)
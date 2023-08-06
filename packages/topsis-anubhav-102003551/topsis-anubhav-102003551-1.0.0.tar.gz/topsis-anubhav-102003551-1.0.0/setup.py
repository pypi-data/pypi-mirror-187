from setuptools import setup, find_packages

setup(
    name = "topsis-anubhav-102003551",
    version = "1.0.0",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type = "text/markdown",
    author = "Anubhav Gupta",
    author_email = "agupta10_be20@thapar.edu",
    url = "https://github.com/anubhav3003/Calco-O-Topsis",
    keywords = ['UCS654', 'TIET'],
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['pandas', 'tabulate'],
    # packages=["topsis"],
    entry_points={
        "console_scripts":[
            "topsis = topsis.__main__:main",
        ]
    },
)
from setuptools import setup, find_packages

setup(
    name = "topsis-sarvagyjain-102003553",
    version = "1.0.1",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type = "text/markdown",
    author = "Sarvagy Jain",
    author_email = "sjain_be20@thapar.edu",
    url = "https://github.com/Sarvagy-Jain/topsis_python_package",
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
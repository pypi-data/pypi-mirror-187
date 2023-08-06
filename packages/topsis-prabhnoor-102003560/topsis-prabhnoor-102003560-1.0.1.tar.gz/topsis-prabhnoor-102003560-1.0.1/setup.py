from setuptools import setup, find_packages

setup(
    name = "topsis-prabhnoor-102003560",
    version = "1.0.1",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type = "text/markdown",
    author = "Prabhnoor Singh Ghotra",
    author_email = "psingh1_be20@thapar.edu",
    url = "https://github.com/Prabhnoor500/topsis_python_package",
    keywords = ['UCS654', 'TIET'],
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['pandas', 'tabulate'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3' 
    ],
    # packages=["topsis"],
    entry_points={
        "console_scripts":[
            "topsis = topsis.__main__:main",
        ]
    },
)
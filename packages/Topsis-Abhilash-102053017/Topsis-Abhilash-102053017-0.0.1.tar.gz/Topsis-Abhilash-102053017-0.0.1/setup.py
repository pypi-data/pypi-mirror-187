from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name = "Topsis-Abhilash-102053017",
    version = "0.0.1",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    author = "Abhilash Jena",
    author_email = "abhilashj02@gmail.com",
    url = "https://github.com/abhi-1407",
    keywords = ['topsis', 'Multicriteria'],
    install_requires = ['pandas', 'tabulate','csv','pandas','math'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3' 
    ],
     entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
     }
)
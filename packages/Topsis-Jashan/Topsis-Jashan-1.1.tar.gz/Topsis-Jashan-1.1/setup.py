from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name = "Topsis-Jashan",
    version = "1.1",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    author = "Jashan Walia",
    author_email = "walia.jashan3@gmail.com",
    url = "https://github.com/Mr-Jashan/Python-Packages/tree/main/Topsis-Jashan",
    keywords = ['Easy to Use', 'Fascinating concept', 'Topsis'],
    packages = ["Topsis-Jashan"],
    include_package_data = True,
    install_requires = ['pandas'],
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
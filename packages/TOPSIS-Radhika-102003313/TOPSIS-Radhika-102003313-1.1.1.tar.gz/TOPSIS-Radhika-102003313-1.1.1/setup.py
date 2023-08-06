from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name = "TOPSIS-Radhika-102003313",
    version = "1.1.1",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    author = "Radhika",
    author_email = "aggarwalradhika9800@gmail.com",
    url = "https://github.com/Radhika980/Topsis-Radhika",
    keywords = ['A simple but powerful decision method'],
    packages = ["TOPSIS-Radhika-102003313"],
    include_package_data = True,
    install_requires = ['pandas'],
        classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6', 
    ],
     entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
     }
)
from setuptools import setup, find_packages

setup(
    name = "topsis-102003553",
    version = "1.1.0",
    license = "MIT",
    description = "A Python package to find TOPSIS for multi-criteria decision analysis method",
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type = "text/markdown",
    author = "Sarvagy Jain",
    author_email = "sarvagyjain @gmail.com",
    url = "https://github.com/Sarvagy-Jain/topsis_python_package",
    keywords = ['UCS538', 'TIET'],
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
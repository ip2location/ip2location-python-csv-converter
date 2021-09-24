import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ip2location-python-csv-converter",
    version="1.0.3",
    description="Python script to converts IP2Location CSV database into IP range or CIDR format.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=['ip2location-csv-converter'],
    author="IP2Location",
    author_email="support@ip2location.com",
    url="https://github.com/ip2location/ip2location-python-csv-converter",
    license='MIT',
    keywords='IP2Location Geolocation',
    project_urls={
        'Official Website': 'https://www.ip2location.com',
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
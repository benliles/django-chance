from os.path import dirname, join

from setuptools import setup, find_packages



version = '0.2'

setup(
    name = 'django-chance',
    version = version,
    description = "Django CMS Plugin for Google Forms",
    long_description = open(join(dirname(__file__), 'README.rst')).read() + "\n" + 
                       open(join(dirname(__file__), 'HISTORY.rst')).read(),
    classifiers = [
        "Framework :: Django",
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License"],
    keywords = 'django cms plugin events conference',
    author = 'Benjamin Liles',
    author_email = 'benliles@gmail.com',
    url = 'https://github.com/benliles/django-chance',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
    ],
)

from os.path import dirname, join

from setuptools import setup, find_packages



version = '0.4.1'

setup(
    name = 'django-chance',
    version = version,
    description = "Django CMS conference application",
    long_description = open(join(dirname(__file__), 'README.rst')).read() + "\n" + 
                       open(join(dirname(__file__), 'HISTORY.rst')).read(),
    classifiers = [
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License"],
    keywords = 'django cms plugin events conference',
    author = 'Benjamin Liles',
    author_email = 'benliles@pytexas.net',
    url = 'https://github.com/pytexas/django-chance',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
    ],
)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PyCFSSL',
    'author': 'Kyle Isom',
    'url': 'https://github.com/kisom/pycfssl',
    'author_email': 'coder@kyleisom.net',
    'version': '0.1',
    'install_requires': ['requests'],
    'packages': ['cfssl'],
    'scripts': [],
    'name': 'pycfssl'
}

setup(**config)

from importlib.machinery import SourceFileLoader
from pathlib import Path
from setuptools import setup

version_module = SourceFileLoader(
    "version", str(Path(__file__).resolve().parent / "behave_web_api" / "version.py")
).load_module()
__version__ = version_module.__version__

long_description = open('README.rst', 'r').read()

install_requires = [
    'behave>=1.2.6,<2.0.0',
    'requests>=2.31.0',
]


setup(
    name='behave-web-api',
    version=__version__,
    packages=['behave_web_api', 'behave_web_api.steps'],
    install_requires=install_requires,
    python_requires='>=3.11',
    description="Provides testing for JSON APIs with Behave",
    long_description=long_description,
    url='https://github.com/jefersondaniel/behave-web-api',
    author='Jeferson Daniel',
    author_email='jeferson.daniel412@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)

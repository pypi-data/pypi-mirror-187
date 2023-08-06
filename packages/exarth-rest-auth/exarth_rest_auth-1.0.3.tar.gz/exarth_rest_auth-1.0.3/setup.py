from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='exarth_rest_auth',
    version='1.0.3',
    description='This library is a fork of the popular django-rest-auth library, with some customizations and '
                'additional features added to suit my specific use case.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Exarth',
    url='https://github.com/saqib-devops/django-rest-auth-exarth-version',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)

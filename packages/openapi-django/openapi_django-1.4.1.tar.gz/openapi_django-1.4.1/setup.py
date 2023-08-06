import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='openapi_django',
    author="Y. Chudakov",
    author_email="kappasama.ks@gmail.com",
    version=os.getenv('RELEASE_VERSION'),
    packages=['openapi_django'],
    package_data={'': package_files(os.path.join(here))},
    description='OpenApi for django',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kappasama.ks/openapi_django',
    install_requires=[
          'Django>=3.2.6', 'djantic==0.7.0', 'pydantic==1.9.1'
     ]
)

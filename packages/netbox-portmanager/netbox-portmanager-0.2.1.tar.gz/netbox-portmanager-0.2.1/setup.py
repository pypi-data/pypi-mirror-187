from setuptools import find_packages, setup

setup(
    name='netbox-portmanager',
    version='0.2.1',
    description='Netbox Plugin - Portmanager',
    long_description='Netbox Plugin - Portmanager',
    url='https://github.com/dansheps/netbox-secretstore/',
    download_url='https://www.pypi.org/project/netbox-secretstore/',
    author='Michal Drobny',
    author_email='ddrobny@ics.muni.cz',
    license='Apache 2.0',
    install_requires=[
        'pysnmp'
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    zip_safe=False,
)
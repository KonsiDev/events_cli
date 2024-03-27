from setuptools import setup, find_packages

setup(
    name='Events-CLI',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    requires_python='>=3.11',
    setup_requires=['setuptools>=68.0.0'],
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'termcolor',
        'importlib_resources',
    ],
    entry_points={
        'console_scripts': [
            'events-cli = src.__main__:main',
        ],
    }
)
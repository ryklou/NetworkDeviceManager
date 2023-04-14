from setuptools import setup, find_packages

setup(
    name='network-device-manager',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={'': ['.gitignore', 'README.md']},
    zip_safe=True,
    install_requires=[
        'Flask==2.1.0',
        'Flask-Migrate==3.1.0',
        'Flask-SQLAlchemy==3.0.3',
        'Flask-WTF==0.15.1',
        'WTForms==3.0.0'
    ],
)

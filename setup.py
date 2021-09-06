from setuptools import setup

setup(
    name='Flask-Container-Frame',
    version='1.0',
    long_description=__doc__,
    packages=['pixiv'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'SQLAlchemy']
)

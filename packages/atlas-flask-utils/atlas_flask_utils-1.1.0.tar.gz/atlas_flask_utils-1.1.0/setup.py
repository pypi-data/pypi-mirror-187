from setuptools import setup, find_packages

setup(
    name='atlas_flask_utils',
    version='1.1.0',
    author='Venfi Oranai',
    author_email='venfioranai@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'flask',
        'marshmallow',
        'werkzeug',
        'sqlalchemy',
        'flask_sqlalchemy',
        'flask_api',
        'flask_restful'
    ]
)

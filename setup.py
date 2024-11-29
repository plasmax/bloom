from setuptools import setup, find_packages

setup(
    name='bloom',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'python-dotenv',
        'flask-sqlalchemy',
        'flask-login',
        'flask-wtf',
        'pyngrok',
        'gunicorn',
        'python-json-logger',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'coverage',
        ],
    },
)

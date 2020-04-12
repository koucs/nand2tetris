import setuptools

setuptools.setup(
    name='janlz',
    version='1.0.0',
    install_requires=["tox"],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'janlz = janlz.main:main'
        ]
    }
)

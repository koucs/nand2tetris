import setuptools

setuptools.setup(
    name='hvmt2',
    version='1.0.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'hvmt2 = hvmt2.main:main'
        ]
    }
)

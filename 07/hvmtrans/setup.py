import setuptools

setuptools.setup(
    name='hvmt',
    version='1.0.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'hvmt = hack_vm_translator.main:main'
        ]
    }
)

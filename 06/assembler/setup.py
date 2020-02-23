import setuptools

setuptools.setup(
    name='asm',
    version='1.0.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'asm = assembler.main:main'
        ]
    }
)

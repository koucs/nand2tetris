import setuptools

setuptools.setup(
    name='asm',
    version='1.0.0',
    packages=setuptools.find_packages(),
    # install_requires=['locustio==0.11.0', 'python-dotenv', 'urllib3', 'pyopenssl', 'boto3', 'influxdb','gevent==1.5a1','python-dateutil==2.8.0', 'ply'],
    entry_points={
        'console_scripts': [
            'asm = assembler.main:main'
        ]
    }
)

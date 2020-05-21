import setuptools

setuptools.setup(
    name='jac',
    version='1.0.0',
    install_requires=["tox", "janlz", "lxml"],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'jac = jac.main:main'
        ]
    }
)

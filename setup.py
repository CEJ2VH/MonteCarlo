from setuptools import setup

setup(
    name = 'MonteCarlo',
    version = '1.0.0',
    author = 'Sarah Hall',
    author_email = 'CEJ2VH@virginia.edu',
    packages = ['MonteCarlo'],
    url = 'https://github.com/CEJ2VH/MonteCarlo',
    license = 'BSD',
    description = 'Packge to create dice, roll them in a game, and analyze the rolls',
    long_description = open('README.md').read(),
    install_requires = [
        "Pandas",
        "NumPy"
    ]
)

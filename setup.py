from setuptools import setup, find_packages

setup(
    name='finance_tracker',
    version='0.1',
    packages=find_packages(),
    py_modules=['cli'],
    install_requires=[
        'click',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'pynance=cli:cli',  # This creates a `finance` command linked to `cli.cli()`
        ],
    },
    author='R. Kyle Norris',
    author_email='r.kyle.norris@gmail.com',
    description='A personal finance tracker CLI tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rkylenorris/PynanceCLI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

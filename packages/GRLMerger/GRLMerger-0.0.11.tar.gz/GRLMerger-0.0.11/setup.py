from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="GRLMerger",
    version='0.0.11',
    description='GRL Merger is a package that allows to merge two GRL models that are written in TGRL syntax.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['grl_merger'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'pandas', 
        'random',
        'statistics',
        'neattext',
        'nltk',
        'sentence_transformers',        
    ],
    author="Nadeen AlAmoudi",
    author_email="<nadeenamoudi1@gmail.com>",
    packages=['grl_merger'],
)
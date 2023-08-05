# -*- coding: utf-8 -*


import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

    setuptools.setup(
        name="arabica",
        version="1.2.1",
        author="Petr Koráb",
        author_email="xpetrkorab@gmail.com",
        packages=["arabica"],
        description="Python package for exploratory text data analysis",
        long_description=description,
        long_description_content_type="text/markdown",
        url="https://github.com/PetrKorab/Arabica",
        python_requires='>=3.8, !=3.11',
        install_requires = ['pandas >=1.4.0',
                            'nltk>3.6.1',
                            'regex',
                            'matplotlib',
                            'matplotlib-inline',
                            'plotnine',
                            'wordcloud',
                            'cleantext>=1.1.4'],
        license='MIT'
    )
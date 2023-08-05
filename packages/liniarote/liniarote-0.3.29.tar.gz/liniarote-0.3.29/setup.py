import setuptools

setuptools.setup(
    name="liniarote",
    version="0.3.29",
    url="https://github.com/NeuraXenetica/liniarote",
    author="Matthew E. Gladden",
    author_email="matthew.gladden@neuraxenetica.com",
    description="The Liniarote package is a command-line interface for the Liniarote programming language, for use in performing operations in transvalent mathematics (i.e., in which division by zero is permitted and generates predictable results, displayed with the aid of the transvalent number symbol “Ƿ”).",
    packages=['liniarote'],
    entry_points={'console_scripts': ['liniarote=liniarote.run:main']},
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'readchar', 'sly'
    ],
)
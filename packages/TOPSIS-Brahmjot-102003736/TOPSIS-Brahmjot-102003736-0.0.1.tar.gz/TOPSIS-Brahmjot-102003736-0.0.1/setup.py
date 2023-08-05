from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1    '
DESCRIPTION = 'TOPSIS-Ranking Algorithm for Multiple Criteria Decision Making'
LONG_DESCRIPTION = 'TOPSIS (Technique for order performance by similarity to ideal solution) is a useful technique in dealing with multi-attribute or multi-criteria decision making (MADM/MCDM) problems in the real world. The principle of compromise (of TOPSIS) for multiple criteria decision making is that the chosen solution should have the shortest distance from the positive ideal solution as well as the longest distance from the negative ideal solution.It compares a set of alternatives based on a pre-specified criterion. The method is used in the business across various industries, every time we need to make an analytical decision based on collected data. \n You input the data in a csv file and then assign weights and impacts of the columns. Applying the Topsis package you will be provded with topsis score and rank along with it.'

# Setting up
setup(
    name="TOPSIS-Brahmjot-102003736",
    version=VERSION,
    author="Brahmjot Kaur",
    author_email="<brahmjotkaur2002@gmail.com >",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['python'],
    keywords=['python', 'TOPSIS', 'MCDM', 'Ranking'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
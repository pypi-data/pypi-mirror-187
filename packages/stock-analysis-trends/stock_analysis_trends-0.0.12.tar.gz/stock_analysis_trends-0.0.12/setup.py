from setuptools import setup, find_packages

VERSION = '0.0.12'
DESCRIPTION = 'Perform stock analysis on Indian and American stocks'
LONG_DESCRIPTION = 'A package that allows to perform analysis and check if a stock is bullish or bearish'

# Setting up
setup(
    name="stock_analysis_trends",
    version=VERSION,
    author="Arjun P",
    author_email="<arjunprakash027@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['yahoofinancials'],
    keywords=['python', 'stock', 'bullish', 'bearish', 'analysis', 'stockmarket'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
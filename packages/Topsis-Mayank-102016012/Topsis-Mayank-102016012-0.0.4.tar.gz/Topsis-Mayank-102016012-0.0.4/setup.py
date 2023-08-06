from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Mayank-102016012", 
    version="0.0.4",
    license='MIT', 
    author="Mayank Rawat",
    author_email="mayank.rawat6802@gmail.com",
    description="Topsis package for MCDM problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.python.org/pypi/Topsis-Mayank-102016012",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.pro:topsis'
        ]
    },
    keywords=['python', 'TOPSIS', 'MCDM', 'MCDA',
              'statistics', 'prescriptive analytics', 'cli'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
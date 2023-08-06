from setuptools import setup,find_packages

with open("E:/6th Sem/Predictive analysis/Topsis-Ravinshu-102003156/README.md", "r") as fh:
    README = fh.read()

setup(
    name='Topsis-Ravinshu-102003156',
    version='1.1.0',
    license='MIT',
    description='A convenient python package for Topsis rank and score calculation for a given dataset, weights and impacts',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='Ravinshu Kushwaha',
    author_email='rv.kushwaha01@gmail.com',
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'topsis=src.topsis:main'
        ]
    },
    keywords=['python', 'TOPSIS', 'MCDM', 'MCDA',
              'statistics', 'prescriptive analytics', 'cli'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

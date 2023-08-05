from distutils.core import setup

with open("PyPi_README.md", "r") as fh:
    readme_desc = fh.read()

setup(
    name='Topsis-Kriti-102017079',
    version='0.2',
    license='MIT',
    description='A convenient python package for Topsis rank and score calculation for a given dataset, weights and impacts',
    long_description=readme_desc,
    long_description_content_type="text/markdown",
    author='Kriti Singhal',
    author_email='kritisinghal711@gmail.com',
    url='https://github.com/Kriti-bit/Topsis-Kriti-102017079',
    download_url='https://github.com/Kriti-bit/Topsis-Kriti-102017079/archive/refs/tags/v0.1.tar.gz',
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

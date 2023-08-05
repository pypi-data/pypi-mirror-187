from distutils.core import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Topsis_Ekaspreet_102017078",
    version="1.0.0",
    description="A Python package implementing TOPSIS for MCDM",
    long_description=readme(),
    author="Ekaspreet kaur",
    author_email="ekaspreet0209@gmail.com",
    url = 'https://github.com/Ekaspreet20/Topsis_Ekas_102017078',
    download_url = 'https://github.com/Ekaspreet20/Topsis_Ekas_102017078/archive/refs/tags/v_01.tar.gz',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=Topsis.topsis:main",
        ]
     },
)

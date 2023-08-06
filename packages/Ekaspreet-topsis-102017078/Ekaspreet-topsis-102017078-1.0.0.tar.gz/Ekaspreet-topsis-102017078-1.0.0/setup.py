from setuptools import setup

def readme():
    with open(r"C:\Users\ekasp\Desktop\Ekaspreet_topsis_102017078\README.md") as f:
        README = f.read()
    return README

setup(
    name="Ekaspreet-topsis-102017078",
    version="1.0.0",
    description="A Python package implementing TOPSIS for MCDM",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Ekaspreet kaur",
    author_email="ekaspreet0209@gmail.com",
    url = 'https://github.com/Ekaspreet20/Ekaspreet_topsis_102017078',
    download_url = 'https://github.com/Ekaspreet20/Ekaspreet_topsis_102017078/archive/refs/tags/v_01.tar.gz',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    
    install_requires=['numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=Topsis.topsis:main",
        ]
     },
     keywords=['python', 'TOPSIS', 'MCDM', 'MCDA',
              'statistics', 'prescriptive analytics', 'cli'],
)

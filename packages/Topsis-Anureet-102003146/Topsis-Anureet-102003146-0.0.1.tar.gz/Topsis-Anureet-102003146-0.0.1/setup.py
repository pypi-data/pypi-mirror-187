from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Topsis-Anureet-102003146",
    version="0.0.1",
    description="TOPSIS Implementation in Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Anureet Kaur",
    author_email="akaur7_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_python"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
     },
)

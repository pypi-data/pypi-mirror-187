from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Topsis-Rishi-102017096",
    version="1.0.0.1",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Rishi Malik",
    author_email="rishi39malik@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_py"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas'
                      ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_py.topsis:main",
        ]
    },
)

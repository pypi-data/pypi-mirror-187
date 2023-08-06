from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Topsis-Tanishq-102003205",
    version="1.1.1",
    description="A Python package to implement Topsis",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Tanishq Singla",
    author_email="tsingla_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main",
        ]
    },
)

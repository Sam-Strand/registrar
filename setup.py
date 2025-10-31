from setuptools import setup, find_packages

setup(
    name="registrar",
    version="1.0.0",
    url="https://github.com/Sam-Strand/registrar",
    author="Садовский М.К.",
    author_email="i@maxim-sadovskiy.ru",
    packages=find_packages(),
    install_requires=[
        "my_id @ git+https://github.com/Sam-Strand/my_id.git",
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
)
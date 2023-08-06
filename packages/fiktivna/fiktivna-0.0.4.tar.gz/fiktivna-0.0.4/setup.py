from setuptools import find_packages, setup

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="fiktivna",
    version="0.0.4",
    url="https://github.com/Laerte/fiktivna",
    project_urls={
        "Documentation": "https://github.com/Laerte/fiktivna",
        "Source": "https://github.com/Laerte/fiktivna",
        "Tracker": "https://github.com/Laerte/fiktivna/issues"
    },
    description="Fiktivna paket",
    long_description=long_description,
    author="Laerte Pereira",
    packages=find_packages(include=["fiktivna*"], exclude=["tests.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    include_package_data=True
)

from setuptools import setup, find_packages

setup(
    name="golf-tempo-trainer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "sounddevice>=0.4.5",
        "soundfile>=0.12.1"
    ],
    python_requires=">=3.7",
) 
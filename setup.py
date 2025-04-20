from setuptools import setup, find_packages

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="total-tempo",
    version="0.1.0",
    author="Dickforeee Golf",
    author_email="contact@dickfore.golf",
    description="A scientifically proven golf swing tempo training system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dickfore/total-tempo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Sports/Training",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
        "sounddevice>=0.4.5",
        "soundfile>=0.12.1",
        "pyttsx3>=2.90"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
            'mypy>=0.900',
            'flake8>=4.0.0',
            'pre-commit>=2.17.0',
        ],
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'pytest-mock>=3.6.0',
            'pytest-timeout>=2.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'total-tempo=total_tempo.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Tracker": "https://github.com/dickfore/total-tempo/issues",
        "Documentation": "https://github.com/dickfore/total-tempo/wiki",
        "Source Code": "https://github.com/dickfore/total-tempo",
    },
) 
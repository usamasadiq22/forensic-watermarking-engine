from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="forensic-watermarking-engine",
    version="1.0.0",
    author="Usama Sadiq",
    author_email="usama@example.com",
    description="A Python-based watermark detection system for identifying embedded watermarks in images and videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usamasadiq/forensic-watermarking-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Security",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "detect-watermark=engine_api:main",
        ],
    },
    keywords="watermark detection forensic image video security",
    project_urls={
        "Bug Reports": "https://github.com/usamasadiq/forensic-watermarking-engine/issues",
        "Source Code": "https://github.com/usamasadiq/forensic-watermarking-engine",
        "Documentation": "https://github.com/usamasadiq/forensic-watermarking-engine#readme",
    },
)

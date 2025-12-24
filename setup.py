#!/usr/bin/env python
"""
PassFoto setup script for installation.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="passfoto",
    version="1.0.0",
    author="PassFoto Team",
    author_email="passfoto@example.com",
    description="A Windows-compatible passport photo enhancement application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alhamdy1/PassFoto",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Editors",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0,<5.0.0",
        "numpy>=1.19.0,<2.0.0",
        "Pillow>=8.0.0,<11.0.0",
    ],
    extras_require={
        "themes": ["ttkthemes>=3.0.0,<4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "passfoto=passfoto.gui:main",
        ],
        "gui_scripts": [
            "passfoto-gui=passfoto.gui:main",
        ],
    },
    include_package_data=True,
    keywords="passport photo enhancement image processing face detection",
    project_urls={
        "Bug Reports": "https://github.com/alhamdy1/PassFoto/issues",
        "Source": "https://github.com/alhamdy1/PassFoto",
    },
)

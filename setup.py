from setuptools import setup
from py_kit.fs import read

setup(
    name="py_kit",
    python_requires=">=3.5",
    version="1.0.0",
    author="SystemLight",
    author_email="1466335092@qq.com",
    maintainer="SystemLight",
    maintainer_email="1466335092@qq.com",
    url="https://github.com/SystemLight/py-kit",
    license="MIT",
    description="Python Tools Collection",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    download_url="https://github.com/SystemLight/py-kit",
    install_requires="",
    platforms=["Windows", "Linux"],
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=[],
    scripts=[],
    entry_points={}
)

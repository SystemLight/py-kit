from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pykit',
    version='1.0.2',
    author='SystemLight',
    author_email='1466335092@qq.com',
    maintainer='SystemLight',
    maintainer_email='1466335092@qq.com',
    url='https://github.com/SystemLight/py-kit',
    download_url='https://github.com/SystemLight/py-kit',
    license='MIT',
    keywords=['kit', 'utils'],
    description='Python Tools Collection',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    platforms=['Windows', 'Linux'],
    python_requires='>=3.9',
    install_requires=[],
    package_data={
        'pykit.tkfoam.sun_valley': ['sun-valley.tcl', 'theme/*.tcl', 'theme/dark/*.png', 'theme/light/*.png'],
    },
    packages=find_packages(exclude=['docs', 'tests*'])
)

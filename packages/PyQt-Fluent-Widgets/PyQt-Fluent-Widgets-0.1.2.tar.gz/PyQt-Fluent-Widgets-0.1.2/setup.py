import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PyQt-Fluent-Widgets",
    version="0.1.2",
    keywords="pyqt fluent widgets",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A library of fluent design widgets",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/zhiyiYo/PyQt-Fluent-Widgets",
    packages=setuptools.find_packages(),
    install_requires=[
        "PyQt5-Frameless-Window",
        "darkdetect",
        "scipy",
        "pillow",
        "colorthief",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)

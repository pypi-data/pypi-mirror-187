from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    requirements = f.readlines()


setup(
    name="Topsis-Aditya-102003706",
    version='0.1.3',
    author='Aditya Aggarwal',
    author_email='aditya.agg7@gmail.com',
    description='Topsis, packaged for ease.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=Topsis.102003706:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=requirements,
    zip_safe=False,
    project_urls={
        'Source': "https://github.com/adityaagg7/Topsis-Package",
        'Tracker': "https://github.com/adityaagg7/Topsis-Package/issues",
    },

)

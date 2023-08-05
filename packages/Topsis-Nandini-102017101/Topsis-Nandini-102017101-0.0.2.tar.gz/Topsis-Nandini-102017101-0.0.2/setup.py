from setuptools import setup

def readme():
    with open('README.md',encoding="utf8") as f:
        README = f.read()
    return README

setup(
    name='Topsis-Nandini-102017101',
    packages=['topsis_package'],
    version='0.0.2',
    license='MIT',
    description='This is a Python Package implementing TOPSIS used for multi-criteria decision analysis method',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Nandini Goel',
    author_email='nandinigoel09@gmail.com',
    keywords=['topsis', 'mcda', 'UCS654', 'TIET'],
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
    ],

    entry_points={
        "console_scripts": [
            "topsis=topsis_package.func:main",
        ]
    },
)
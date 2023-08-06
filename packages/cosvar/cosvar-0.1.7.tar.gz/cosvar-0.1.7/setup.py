from setuptools import setup, find_packages

# https://levelup.gitconnected.com/turn-your-python-code-into-a-pip-package-in-minutes-433ae669657f
# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'cosvar',
    version = '0.1.7',    
    description = 'Python Cosmic Variance Calculator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/astrockragh/pyCV',
    author='Christian Kragh Jespersen',
    author_email='ckragh@princeton.edu',
    license='MIT',
    packages=['cosvar'],
    # packages = find_packages(),
    install_requires=['pandas',
                      'numpy',                     
                      'scipy'],

    classifiers=['Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',    
        'Programming Language :: Python :: 3.8']
)
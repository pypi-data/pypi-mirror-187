from setuptools import setup,find_packages
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
   'Programming Language :: Python :: Implementation :: PyPy',
]
setup(
    name='simple_calculator_by_DT',
    version='1.0.0',
    description='this is simple calculator package for practise',
    author='Davor Telisman',
    author_email='davor.python@gmail.com',
    url='https://github.com/Telisman/Python-Package.git',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    classifiers = classifiers,
    keywords='calculator',
    install_requires=['setuptools>=56','pip>= 22.0.4'],
)
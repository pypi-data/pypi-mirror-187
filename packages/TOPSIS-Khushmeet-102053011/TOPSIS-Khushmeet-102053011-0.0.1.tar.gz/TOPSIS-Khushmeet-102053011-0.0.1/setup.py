from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS-Khushmeet-102053011',
  version='0.0.1',
  description='It is used for calculating topsis score and rank.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/khushmeetkj/topsis.git',  
  author='Khushmeet Kaur',
  author_email='khushmeet.kj@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)
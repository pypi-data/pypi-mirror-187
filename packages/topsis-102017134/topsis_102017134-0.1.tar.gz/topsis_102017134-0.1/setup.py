from setuptools import setup
setup(
  name = 'topsis_102017134',         
  packages = ['topsis_102017134'],   
  version = '0.1',      
  license='MIT',       
  description = 'A topsis package',   
  author = 'Soumya Srivastava',                  
  author_email = 'ssrivastava_be20@thapar.edu',      
  url = 'https://github.com/sri-soumya/topsis',   
  keywords = ['thapar', 'ucs654', 'topsis'],  
  install_requires=[           
          'pandas',
          'numpy',
          'sys'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
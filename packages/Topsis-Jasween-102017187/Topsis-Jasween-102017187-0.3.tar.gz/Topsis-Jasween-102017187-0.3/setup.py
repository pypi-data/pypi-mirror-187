from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
  name = 'Topsis-Jasween-102017187',        
  packages = ['topsis'],   
  version = '0.3',    
  license = 'MIT',      
  description = 'Topsis-Jasween-102017187 is a Python library to solve Multiple Criteria Decision Making(MCDM) problems by using TOPSIS',   
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Jasween Kaur Brar',                  
  author_email = 'jbrar_be20@thapar.edu',      
  url = 'https://github.com/JasweenBrar/Topsis-Jasween-102017187', 
  install_requires=[          
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
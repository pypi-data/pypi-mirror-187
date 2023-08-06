from setuptools import setup,find_packages
setup(
  name = 'Topsis-ParvGupta-102017186',         
  #packages = ['Topsis-ParvGupta-102017186'],   
  version = '1.0.0',      
  license='MIT',        
  description = 'A command line python program to implement the Topsis',   
  author = 'Parv Gupta',                   
  author_email = 'pgupta4_be20@thapar.edu',      
  keywords = ['Topsis', 'Multiple Criteria'],  
  packages = find_packages(),
  install_requires=[            
          'pandas',
          'numpy',
          'sys',
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

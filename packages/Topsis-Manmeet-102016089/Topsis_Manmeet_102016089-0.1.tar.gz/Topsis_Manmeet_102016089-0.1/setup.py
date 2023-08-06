from distutils.core import setup
setup(
  name = 'Topsis_Manmeet_102016089',
  packages = ['Topsis_Manmeet_102016089'],   
  version = '0.1',    
  license='MIT',        
  description = 'Topsis Implementation',
  author = 'Manmeet Singh',
  author_email = 'msingh5_be20@thapar.edu',
  keywords=['topsis'],
   install_requires=[            # I get to this in a second
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
  ],
)
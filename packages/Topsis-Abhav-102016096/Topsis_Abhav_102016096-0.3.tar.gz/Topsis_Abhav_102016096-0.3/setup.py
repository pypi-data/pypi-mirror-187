from distutils.core import setup
setup(
  name = 'Topsis_Abhav_102016096',         
  packages = ['Topsis_Abhav_102016096'],   
  version = 'v0.3',      
  license='MIT',        
  description = 'A topsis score and ranks calculator package', 
  long_description='''# Topsis-Calculator
## The efficient python package to calcualate topsis scores

Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria-based decision-making method. TOPSIS chooses the alternative of shortest the Euclidean distance from the ideal solution and greatest distance from the negative ideal solution. 

To make this definition easier, let's suppose you want to buy a mobile phone, you go to a shop and analyze 5 mobile phones on basis of RAM, memory, display size, battery, and price. At last, you’re confused after seeing so many factors and don’t know how to decide which mobile phone you should purchase. TOPSIS is a way to allocate the ranks on basis of the weights and impact of the given factors.

## Features

- Imports an input csv file and calculates Topsis scores and ranks of it
- Output file consists of seaparate columns as Topsis scores and Ranks which is ideal for decision making



And of course Topsis itself is open source with a [public repository](https://github.com/abhavgoel/base-Topsis-Abhav-102016096)
 on GitHub.

## Installation

Topsis requires [Python](https://www.python.org/downloads/) v3+ to run.
Use pip to install the package.

```sh
pip install Topsis-Abhav-102016096
```
## Usage
```sh
import Topsis_Abhav_102016096 as tp
#call for topsis_score function
tp.topsis_score("input.csv","weights","impact","output.csv")
```
- Make sure you enter "weights" and "impact" as string
- The result would be stored in a output csv file with ranks and topsis score respectively.

## Example
input.csv
| Model | corr | R2  | Rmse | Acc |
| --- | --- | --- | --- | --- |
| m1  | 0.79 | 0.62 | 1.25 | 60.89 |
| m2  | 0.66 | 0.44 | 2.89 | 63.07 |
| m3  | 0.56 | 0.31 | 1.57 | 62.87 |
| m4  | 0.82 | 0.67 | 2.68 | 70.19 |
| M5  | 0.75 | 0.56 | 1.3 | 80.39 |

output.csv
| Model | corr | R2  | Rmse | Acc | Topsis score | Rank |
| --- | --- | --- | --- | --- | --- | --- |
| m1  | 0.79 | 0.62 | 1.25 | 60.89 | 0.7722097345612788 | 2   |
| m2  | 0.66 | 0.44 | 2.89 | 63.07 | 0.22559875426413367 | 5   |
| m3  | 0.56 | 0.31 | 1.57 | 62.87 | 0.43889731728018605 | 4   |
| m4  | 0.82 | 0.67 | 2.68 | 70.19 | 0.5238778712729114 | 3   |
| M5  | 0.75 | 0.56 | 1.3 | 80.39 | 0.8113887082429979 | 1   |

- The output csv contains the ranks of all the rows i.e. Model M5 is the best among the others




## License

MIT

**Free Software, Hell Yeah!**

''',
  long_description_content_type='text/markdown',
  author = 'Abhav Goel',                   
  author_email = 'goelabhav2002@gmail.com',     
  
  keywords = ['topsis'],   
  install_requires=[           
          'numpy',
          'pandas',
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
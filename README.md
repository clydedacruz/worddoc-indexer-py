# worddoc-indexer-py

## Dependencies
Python version: Use python version 3.5 or greater

To install dependencies, run : `pip install nltk` 

Then download nltk data : in the python prompt:  
```
import nltk
nltk.download('wordnet')
```

## Usage

To create index : `python create_index.py data`

To query : `python query_index.py <term1> <term2> ...<termN>`
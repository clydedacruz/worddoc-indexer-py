__author__ = "Clyde D'Cruz"
__license__ = "GPL"

# Install dependencies
# pip install -r requirements.txt
# download nltk data
# nltk.download('wordnet')

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import os
import bisect
import json
import nltk
import sys
# run->  nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

ENGLISH_STOPWORDS = set(["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"])

def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

def removeStopwords(wordlist):
    return [set(wordlist) - ENGLISH_STOPWORDS]


if len(sys.argv) < 2:
    print("Missing argument. Expected input docs directory as argument.\nEg: python create_index.py data")
    sys.exit()

input_docs_dir = sys.argv[1]
INDEX_FILE = "INDEX_FILE.INDEX"


indexFile = open(INDEX_FILE,'w')
indexDictionary = {}

lemmatizer = WordNetLemmatizer()


def addToPostings(postings, docid):
    bisect.insort(postings, docid)
    return postings


for filename in os.listdir(input_docs_dir):
    if filename.endswith(".docx"):
        doc_text = get_docx_text(os.path.join(input_docs_dir,filename))
        
        word_tokens = doc_text.split(' ')     

        for w in word_tokens:

            # exclude stopwords
            if w in ENGLISH_STOPWORDS:
                continue
            
            lem_word = lemmatizer.lemmatize(w)

            #add to index
            try:
                term_info = indexDictionary[lem_word]
                if filename in term_info['postings']:
                    continue
                term_info['df'] += 1
                term_info['postings'] = addToPostings(term_info['postings'],filename)
            except KeyError:
                # Key is not present
                indexDictionary[lem_word] = {'df': 1,'postings':[filename]}

index_as_string = json.dumps(indexDictionary, sort_keys = True)
indexFile.write(index_as_string)
print("Index file created at INDEX_FILE.INDEX")
print("Index stats\n"+'-'*50)
print("Number of terms: "+ str(len(indexDictionary)))

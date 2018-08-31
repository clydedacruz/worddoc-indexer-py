__author__ = "Clyde D'Cruz"
__license__ = "GPL"

from nltk.stem import WordNetLemmatizer
import sys
import json

ENGLISH_STOPWORDS = set(["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"])
def removeStopwords(wordlist):
    return [set(wordlist) - ENGLISH_STOPWORDS]


INDEX_FILE = "INDEX_FILE.INDEX"
# read index file into memory 
index = open(INDEX_FILE)
indexDictionary = json.loads(index.read())

lemmatizer = WordNetLemmatizer()


def set_list_intersection(set_list):
  if not set_list:
    return set()
  result = set_list[0]
  for s in set_list[1:]:
    result &= s
  return result


# get query as args 
query_terms = sys.argv[1:]
normalized_query = []
result_sets = []
print('_'*50+"\nQuery Result \n"+ '_'*50)
for w in query_terms:

    # remove stop words from query terms
    if w in ENGLISH_STOPWORDS:
        continue
    # lemmatize query terms
    lem_word = lemmatizer.lemmatize(w)
    # normalized_query.append(lem_word)
    try:
        result_sets.append(set(indexDictionary[lem_word]['postings']))
    except:
        print("No documents found matching query : "+ ' '.join(query_terms))
        break

query_result = set_list_intersection(result_sets)
if len(query_result) > 0:
    print('\n'.join(list(query_result)))

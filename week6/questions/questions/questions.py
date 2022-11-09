import nltk
import sys
import os
import math 
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 5


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    
    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens


    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory,filename),encoding="utf8") as f:
            result[filename] = f.read()

    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    token_list = [ word.lower() for word in nltk.word_tokenize(document)
    if any(c.isalpha() for c in word)]

    for word in token_list:
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            token_list.remove(word)

    return token_list

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for filename in documents:
        words.update(documents[filename])

    idf = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf_value = 1 + math.log(len(documents)/f)
        idf[word] = idf_value

    return idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf_value_files = list()
    for filename in files:
        sum_tfidf = 0
        for word in query:
            tf = files[filename].count(word)
            tfidf = tf * idfs[word]
            sum_tfidf += tfidf
        tfidf_value_files.append((filename,sum_tfidf))

    
    tfidf_value_files.sort(key=lambda t: t[1], reverse=True)

    tfidf_files_list = []
    for filename in tfidf_value_files:
        tfidf_files_list.append(filename[0])

    return tfidf_files_list[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_value_files = list()
    for sentence in sentences:
        sum_idf = 0
        density = 0
        for word in query:
            if word in sentences[sentence]:
                sum_idf += idfs[word]
                density += 1
        term = density/len(sentences[sentence])

        idf_value_files.append((sentence,sum_idf,term)) 

    idf_value_files.sort(key=lambda t:(t[1],t[2]), reverse=True)

    result = []
    for sentence in idf_value_files:
        result.append(sentence[0])
    
    return result[:n]

if __name__ == "__main__":
    main()

import os
import random
import re
import sys
from pomegranate import *
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}
    if len(corpus[page]) == 0:
        for source_page in corpus: 
            result[source_page] = 1/len(corpus)
    else:
        for source_page in corpus:
            if source_page in corpus[page]:
                result[source_page] = damping_factor/len(corpus[page]) + (1 - damping_factor)/len(corpus)
            else:
                result[source_page] = (1 - damping_factor)/len(corpus)
    return result
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_dict ={}
    for page in corpus:
        start_dict[page] = 1 / len(corpus)
    start = DiscreteDistribution(start_dict)

    big_list=[]
    for page in corpus:
        each_dict_prob = transition_model(corpus,page,damping_factor)
        for link_page in each_dict_prob:
            list_each = [page,link_page,each_dict_prob[link_page]]
            big_list.append(list_each)

    transition = ConditionalProbabilityTable(big_list,[start])

    model = MarkovChain([start, transition])
    sample = model.sample(n)

    result_dict = {}
    for page in corpus:
        result_dict[page] = 0

    for page in sample:
        result_dict[page] += 1

    for page in result_dict:
        result_dict[page] /= n

    return result_dict


    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_result = {}
    for page in corpus:
        current_result[page] = 1 / len(corpus)
        
    new_result = {}
    for page in corpus:
        new_result[page] = (1 - damping_factor) / len(corpus)
        
        for page_rest in corpus:
            if page_rest == page:
                continue
            else:
                if page in corpus[page_rest]:
                    new_result[page] += damping_factor * (current_result[page_rest] / len(corpus[page_rest]))



    for page in current_result:
        if abs(current_result[page] - new_result[page]) >= 0.001:
            compare = False
        else:
            compare = True
   
    while compare == False:
        current_result = new_result.copy()
        new_result = {}
        for page in corpus:
            new_result[page] = (1 - damping_factor) / len(corpus)
        
            for page_rest in corpus:
                if page_rest == page:
                    continue
                else:
                    if page in corpus[page_rest]:
                        new_result[page] += damping_factor * (current_result[page_rest] / len(corpus[page_rest]))
        
        for page in current_result:
            if abs(current_result[page] - new_result[page]) >= 0.001:
                compare = False
            else:
                compare = True
    return new_result

    raise NotImplementedError


if __name__ == "__main__":
    main()

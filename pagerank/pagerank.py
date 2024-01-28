import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100000
rank = -1
pagerank = {}

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

    length = len(corpus)
    length_page = len(corpus[page])
    
    probabilities = {} 
    
    if length_page != 0:
        for key in corpus:
            probabilities[key] = (1 - damping_factor) / length
            
        for key in corpus[page]:
            probabilities[key] += damping_factor / length_page
    else: 
        for key in corpus:
            probabilities[key] = 1 / length
        
    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for key in corpus:
        pagerank[key] = 0
    
    page = random.choice(list(corpus))
    
    for _ in range(n):
        pagerank[page] += 1
        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

    for key in pagerank:
        pagerank[key] = pagerank[key] / n
        
    return pagerank
    
def calculate_pr(corpus, p, damping_factor):
    global pagerank
    #Maps every link to current page to their count of total links
    links = {}
    check = False
    for key in corpus:
        counter = 0
        for value in corpus[key]:
            counter += 1
            if value == p:
                check = True
        if check:
            links[key] = counter
            check = False
            
    corpus_length = len(corpus)
    
    pr = (1 - damping_factor) / corpus_length
    sigma = 0
    
    for link in links:
        sigma += pagerank[link] / links[link]      
    pr += damping_factor * sigma
    
    if (max(pr, pagerank[p]) - min(pr, pagerank[p])) < 0.00001:
        return True
    
    pagerank[p] = pr 
    return False
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    length = len(corpus)
    for page in corpus:
        pagerank[page] = 1 / length
    
    flag = True
    while flag:  
        if not flag:
            break
        
        for page in pagerank:
            if calculate_pr(corpus, page, damping_factor):
                flag = False
                
    return pagerank
     

if __name__ == "__main__":
    main()
    


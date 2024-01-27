import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
rank = -1

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
    
def calculate_pr(corpus, page, damping_factor):
    global rank
    length = len(corpus)
    links = [key for key, value in corpus.items() if page in value]
    
    pr = (1 - damping_factor) / length
    sigma = 0
    for link in links:
        sigma += rank / len(links) 
    pr += damping_factor * sigma
    print(pr)
    
    if (max(pr, rank) - min(pr, rank) < 0.001):
        return pr
    
    rank = pr 
    return calculate_pr(corpus, page, damping_factor)     

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    length = len(corpus)
    global rank
    
    for i in corpus:
        pagerank[i] = 1 / length
    
    while True:
        
    #Dumbass you dont calculate pr(i) for i that links to page,
    #you calculate it for rank of current page, fix it 
    return pagerank

if __name__ == "__main__":
    main()
    #iterate_pagerank(crawl(sys.argv[1]), DAMPING)
    #print(sample_pagerank(crawl(sys.argv[1]), DAMPING, 1000))
    #print(pr(crawl(sys.argv[1])), "1.html", DAMPING, )
    #print(calculate_pr(crawl(sys.argv[1]), "1.html", DAMPING))
    
















"""
    pr = (1 - damping_factor) / length
    while switch:
        for page in pagerank: 
            links = []
            for key, value in corpus.items():
                if value == page:
                    links.append(key)
                    
            pr = (1 - damping_factor) / length
            sigma = 0
            for i in links: 
                print(i)
                sigma += pagerank[i] / len(i)
            pr += damping_factor * sigma
            
            if max(pr, pagerank[page]) - min(pr, pagerank[page]) < 0.001:
                switch = False

            pagerank[key] = pr
        
    print(pagerank)
    return pagerank   
    """
    
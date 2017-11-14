from pybloomfilter import BloomFilter
import os
import re

# Read all my posts.
posts = {post_name: open(POST_DIR + post_name).read() for post_name in os.listdir(POST_DIR)}
# Create a dictionary of {"post name": "lowercase word set"}.
split_posts = {name: set(re.split("\W+", contents.lower())) for name, contents in posts.items()}

filters = {}
for name, words in split_posts.items():
    filters[name] = BloomFilter(capacity=len(words), error_rate=0.1)
    for word in words:
        filters[name].add(word)

def search(search_string):
    search_terms = re.split("\W+", search_string)
    return [name for name, filter in filters.items() if all(term in filter for term in search_terms)]

def main():
 	str=input("Search for: ")
 	print(search(str))
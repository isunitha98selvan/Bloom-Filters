# Bloom-Filters

Bloom filters are a probablistic data structure which are used to determine with certainity whether an element is not present in a set or determine with a certain probablility if the element is present in the set.

##Python Implementation of Accurate Counting Bloom Filters
We use ACBF to reduce the false positive probability.We implement ACBFs in MapReduce to improve the reduce-side join performance. ACBF is used in the map phase to filter out redundant records shuffled. ACBF is constructed in a distributed way by merging local hash tables of all map tasks. 

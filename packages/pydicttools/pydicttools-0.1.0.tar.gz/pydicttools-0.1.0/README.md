### Python Dictionary Utility Package

This package contains a collection of functions that perform various operations on Python dictionaries.

#### Features

##### concat_dict(dict1, dict2):

Takes two dictionaries as input and returns a new dictionary that is the result of merging the keys and values of both input dictionaries.

##### key_exists(dictionary, key):

Takes a dictionary and a key as input and returns a Boolean indicating whether the key exists in the dictionary.

##### value_exists(dictionary, value):

Takes a dictionary and a value as input and returns a Boolean indicating whether the value exists in the dictionary.

##### clone(obj):

Takes an object as input and returns a deep copy of the object.

##### is_empty(dictionary):

Takes a dictionary as input and returns a Boolean indicating whether the dictionary is empty.

get_value_from_dict(dictionary, key_path):
Takes a dictionary and a key path as input and returns the value associated with the key path.

##### is_subset(dict1, dict2):

Takes two dictionaries as input and returns a Boolean indicating whether dict1 is a subset of dict2.

##### sort_dict_by_key(d):

Takes a dictionary as input and returns a new dictionary with the items sorted by key.

##### sort_dict_by_custom_key(d, key_extractor):

Takes a dictionary and a key extractor function as input and returns a new dictionary with the items sorted by the custom key extractor.

##### pretty_print_dict(d, indent):

Takes a dictionary and an indentation level as input and pretty prints the dictionary.

##### iterate_dict(d):

Takes a dictionary as input and returns an iterator over the key-value pairs of the dictionary.

##### clone_async(obj):

Takes an object as input and returns a deep copy of the object asynchronously.

#### Installation

To install the package, run the following command:

```python
pip install pydicttool
```

#### Usage

```python
from python_dictionary_utility import *

dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

# Concatenate two dictionaries
result = concat_dict(dict1, dict2)
print(result) # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Check if key exists in dictionary
result = key_exists(dict1, 'a')
print(result) # True

# Check if value exists in dictionary
result = value_exists(dict1, 2)
print(result) # True

# Clone object
result = clone({'a': [1, 2, 3]})
print(result) # {'a': [1, 2, 3]}

# Check if dictionary is empty
result = is_empty({})
print(result) # True

# Get value from dictionary by key path
result = get_value_from_dict({'a': {'b': {'c': 1}}}, 'a.b.c')
print(result) # 1

# Check if one dictionary is subset of another
original_dict = {'c': 3, 'a': 1, 'b': 2}
sorted_dict = sort_dict_by_key(original_dict)
print(sorted_dict) # {'a': 1, 'b': 2, 'c': 3}

original_dict = {'c': 3, 'a': 1, 'b': 2}

# Custom key extractor function
def custom_key_extractor(key, value):
    return value

sorted_dict = sort_dict_by_custom_key(original_dict, custom_key_extractor)
print(sorted_dict) # {'a': 1, 'b': 2, 'c': 3}

original_dict = {'c': 3, 'a': 1, 'b': 2}
pretty_print_dict(original_dict, 2)
# Output:
# {
#   "a": 1,
#   "b": 2,
#   "c": 3
# }

original_dict = {'c': 3, 'a': 1, 'b': 2}
for key, value in iterate_dict(original_dict):
    print(f'{key}: {value}')
# Output:
# c: 3
# a: 1
# b: 2
``

# Clone object
result = clone({'a': [1, 2, 3]})
print(result) # {'a': [1, 2, 3]}

```

##### clone_async example usage for python 3.8>=

```python
import asyncio

# Original object
original_obj = {'a': [1, 2, 3], 'b': {'c': 4, 'd': 5}}

async def main():
    # Asynchronously clone the object
    cloned_obj = await clone_async(original_obj)

    # Print the cloned object
    print(cloned_obj) # {'a': [1, 2, 3], 'b': {'c': 4, 'd': 5}}

# Run the main function
await main()

```

##### clone_async example usage for python 3.7<

```python
import asyncio

# Original object
original_obj = {'a': [1, 2, 3], 'b': {'c': 4, 'd': 5}}

async def main():
    # Asynchronously clone the object
    cloned_obj = await clone_async(original_obj)

    # Print the cloned object
    print(cloned_obj) # {'a': [1, 2, 3], 'b': {'c': 4, 'd': 5}}

# Run the main function
asyncio.run(main())
```

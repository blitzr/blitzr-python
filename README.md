Blitzr Python Client
================


This package makes it easy to call the Blitzr API. You can find the complete package documentation [here](http://blitzr.github.io/blitzr-python/). 
You can also refer to the official [Blitzr API reference](https://api.blitzr.com/doc) to have more informations.

----------


Installation
---------------

You can simply install Blitzr by **pip**:

```
pip install blitzr
```
----------

Getting Started
---------------------

You just need to instanciate a **BlitzrClient** and call its methods.

**Example**

```python
from blitzr import BlitzrClient

blitzr = BlitzrClient(your_api_key)

eminem = blitzr.get_artist(slug='eminem')
print eminem.get('real_name')

# prints
# Marshall Bruce Mathers III
```

You can call list APIs by two methods: with or without a generator.

The basic methods like **get_artist_releases** returns a list or X desired releases from the given artist. You will have to manage the pagination by yourself with the **start** and **limit** parameters (defaults are start=0 and limit=10).

**Example**

```python
from blitzr import BlitzrClient

blitzr = BlitzrClient(your_api_key)

releases = blitzr.get_artist_releases(slug='eminem')
for release in releases:
    print release.get('name')

# prints
#
# Marshall Bruce Mathers III
# The Vinyl LPs
# MNEP
# Live From Comerica Park
# Phenomenal
# Detroit Vs. Everybody
# Shady Classics Mixtape
# Headlights
# Guts Over Fear
# The Monster
# Berzerk
```

The second option will make the pagination easier. You can call the **iter_artist_releases** to get a **generator**. This generator will call automatically the API when you reach the end of the current items list. So you just have to iterate on this generator to get all the documents to retrieve. The parameter **limit** here is the number of elements to retrieve by query in the generator.

**Example**

```python
from blitzr import BlitzrClient

blitzr = BlitzrClient(your_api_key)

releases = blitzr.iter_artist_releases(slug='eminem')
for release in releases:
    print release.get('name')

# prints
#
# Marshall Bruce Mathers III
# The Vinyl LPs
# MNEP
# Live From Comerica Park
# Phenomenal
# Detroit Vs. Everybody
# Shady Classics Mixtape
# Headlights
# Guts Over Fear
# The Monster
# Berzerk
# Rap God
# Survival
# The Marshall Mathers LP 2
# E
# Shady Unit
# Eminem The Marshall Mathers
#
# ... and more until the end

```

----------

SearchGenerator
-----------------------

The **SearchGenerator** is a custom Generator for **Search requests** that provides **length compatibility.**

The only non standard generators are those returned by the search queries. They are differents by their ability to retreive the total count of elements to generate.

You will be able to call the **len()** method on the generator.

**Example**

```python
from blitzr import BlitzrClient

blitzr = BlitzrClient(your_api_key)

artists = blitzr.search_iter_artist(query='emine', autocomplete=True)

print len(artists)

# prints
#
# 80
```

Then it works exactly as all other generators.

**Example**

```python
for artist in artists:
    print artist.get('name')
# prints
#
# Emine
# Emine
# Eminem
# Emine Krasniqi
# Eminence
# Eminent
# Eminent
# ...
```

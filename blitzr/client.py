#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Blitzr Python Client
    ====================

    This package makes it easy to call the Blitzr API.
    You can refer to the official [Blitzr API reference](http://api.blitzr.com/doc)
    to have more informations.


    Installation
    ------------

    You can simply install Blitzr by pip:

        pip install blitzr


    Getting Started
    ---------------

    You just need to instanciate a **BlitzrClient** and call its methods.

    :Example:

    >>> from blitzr import client
    >>> blitzr = client.BlitzrClient(your_api_key)
    >>> eminem = blitzr.get_artist(slug='eminem')
    >>> print eminem.get('real_name')
    Marshall Bruce Mathers III

    The lists APIs use generators.

    :Example:

    >>> from blitzr import client
    >>> blitzr = client.BlitzrClient(your_api_key)
    >>> releases = blitzr.get_artist_releases(slug='eminem')
    >>> for release in releases:
    >>>     print release.get('name')
    The Vinyl LPs
    MNEP
    Live From Comerica Park
    Phenomenal
    Detroit Vs. Everybody
    Shady Classics Mixtape
    ...

"""

import requests
from .exceptions import (ConfigurationException, ServerException, ClientException, NetworkException)

class BlitzrClient(object):
    """BlitzrClient

    This is the only class you need to call the Blitzr API.

    """

    BASE_URL = "https://api.blitzr.com/"

    def __init__(self, api_key):
        """Construct the BlitzrClient with your API key."""
        if api_key:
            self.api_key = api_key
        else:
            raise ConfigurationException('api_key is missing.')

    def _request(self, method, params):
        """Base method to call the API with given params."""
        url = self.BASE_URL + method
        params['key'] = self.api_key
        try:
            req = requests.get(url=url, params=params)
            req.raise_for_status()
            return req.json()
        except requests.exceptions.HTTPError:
            if req.status_code >= 500:
                raise ServerException(
                    'An error occured on the Blitzr side. HTTP code: ' + str(req.status_code)
                    )
            elif req.status_code >= 400:
                raise ClientException(req.json())
        except requests.exceptions.ConnectionError as exception:
            raise NetworkException(str(exception))


###############################
##          Artists          ##
###############################


    def get_artist(self, uuid=None, slug=None, extras=[], extras_limit=None):
        """Get an Artist from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param extras: Artist extras : aliases, websites, biography, last_releases,
            next_events, relations
        :param extras_limit: Limit for iterable extras : last_releases, next_events (max is 10)
        :type uuid: string
        :type slug: string
        :type extras: array
        :type extras_limit: int
        :return: Artist
        :rtype: dictionary

        """
        return self._request('artist/', {
            'uuid'         : uuid,
            'slug'         : slug,
            'extras'       : ','.join(extras) if extras else None,
            'extras_limit' : extras_limit
        })

    def get_artist_aliases(self, uuid=None, slug=None):
        """Get an Artist's aliases from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :type uuid: string
        :type slug: string
        :return: Artists
        :rtype: generator

        """
        for alias in self._request('artist/aliases/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield alias

    def get_artist_bands(self, uuid=None, slug=None, start=0, limit=10):
        """Get an Artist's bands from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :return: Artists
        :rtype: generator

        """
        while True:
            bands = self._request('artist/bands/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for band in bands:
                yield band
            start += limit
            if len(bands) < limit:
                break

    def get_artist_biography(self, uuid=None, slug=None, lang=None, html_format=False,
                             url_scheme=None):
        """Get an Artist's biography from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param lang: Biography language (if available) (fr|en)
        :param html_format: True for HTML markup in the biography
        :param url_scheme: Urlencoded links format
        :type uuid: string
        :type slug: string
        :type lang: string
        :type html_format: bool
        :type url_scheme: string
        :return: Biography
        :rtype: dictionary

        """
        return self._request('artist/biography/', {
            'slug'       : slug,
            'uuid'       : uuid,
            'lang'       : lang,
            'format'     : 'html' if html_format else None,
            'url_scheme' : url_scheme
        })

    def get_artist_events(self, uuid=None, slug=None, start=0, limit=10):
        """Get an Artist's events from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :return: Events
        :rtype: generator

        """
        while True:
            events = self._request('artist/events/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for event in events:
                yield event
            start += limit
            if len(events) < limit:
                break

    def get_artist_members(self, uuid=None, slug=None, start=0, limit=10):
        """Get a Band's members from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :return: Artists
        :rtype: generator

        """
        while True:
            members = self._request('artist/members/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for member in members:
                yield member
            start += limit
            if len(members) < limit:
                break

    def get_artist_related(self, uuid=None, slug=None, start=0, limit=10):
        """Get related Artists from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :return: Artists
        :rtype: generator

        """
        while True:
            related = self._request('artist/related/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for artist in related:
                yield artist
            start += limit
            if len(related) < limit:
                break

    def get_artist_releases(self, uuid=None, slug=None, start=0, limit=10, release_type=None,
                            release_format=None, credited=False):
        """Get an Artist's releases from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :param release_type: Release type (official|unofficial|all)
        :param release_format: Release format (album|single|live|all)
        :param credited: Releases where artist is credited (not main releases)
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :type release_type: string
        :type release_format: string
        :type credited: bool
        :return: Releases
        :rtype: generator

        """
        while True:
            releases = self._request('artist/releases/', {
                'uuid'      : uuid,
                'slug'      : slug,
                'start'     : start,
                'limit'     : limit,
                'type'      : release_type,
                'format'    : release_format,
                'credited'  : 'true' if credited else 'false'
            })
            for release in releases:
                yield release
            start += limit
            if len(releases) < limit:
                break

    def get_artist_similar(self, uuid=None, slug=None, filters=[], start=0, limit=10):
        """Get similar Artists from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param filters: Filter results. Available filters : location
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type filters: array
        :type start: int
        :type limit: int
        :return: Artists
        :rtype: generator

        """
        while True:
            similar = self._request('artist/similars/', {
                'uuid'      : uuid,
                'slug'      : slug,
                'filters'   : ','.join(filters)if filters else None,
                'start'     : start,
                'limit'     : limit
            })
            for artist in similar:
                yield artist
            start += limit
            if len(similar) < limit:
                break

    def get_artist_summary(self, uuid=None, slug=None):
        """Get an Artist's summary from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :type uuid: string
        :type slug: string
        :return: Summary
        :rtype: dictionary

        """
        return self._request('artist/summary/', {
            'uuid'  : uuid,
            'slug'  : slug,
        })

    def get_artist_websites(self, uuid=None, slug=None):
        """Get Artist's websites from the Blitzr API.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :type uuid: string
        :type slug: string
        :return: Websites
        :rtype: generator

        """
        for website in self._request('artist/websites/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield website


###############################
##           Events          ##
###############################

    def get_event(self, uuid=None, slug=None):
        """Get an Event from the Blitzr API.

        :param uuid: The Event UUID
        :param slug: The Event Slug
        :type uuid: string
        :type slug: string
        :return: Event
        :rtype: dictionary

        """
        return self._request('event/', {
            'uuid'  : uuid,
            'slug'  : slug,
        })

    def get_events(self, country_code=None, latitude=None, longitude=None, city=None, venue=None,
                   tag=None, date_start=None, date_end=None, radius=None, start=0, limit=10):
        """Search Events from the Blitzr API.

        :param country_code: The official country code
        :param latitude: Latitude of a reference geopoint (use with radius)
        :param longitude: Longitude of a reference geopoint (use with radius)
        :param city: City where the event takes place (not compatible with country code)
        :param venue: Venue where the event takes place
        :param tag: Tag filter
        :param dateStart: Date minimum
        :param dateEnd: Date maximum
        :param radius: Distance max from the reference geopoint (in km)
        :param start: Offset for pagination
        :param limit: Limit for pagination
        :type country_code: string
        :type latitude: float
        :type longitude: float
        :type city: string
        :type venue: string
        :type tag: string
        :type dateStart: date
        :type dateEnd: date
        :type radius: int
        :type start: int
        :type limit: int
        :return: Events
        :rtype: generator

        """
        while True:
            events = self._request('events/', {
                'country_code'  : country_code,
                'latitude'      : latitude,
                'longitude'     : longitude,
                'city'          : city,
                'venue'         : venue,
                'tag'           : tag,
                'date_start'    : date_start,
                'date_end'      : date_end,
                'radius'        : radius,
                'start'         : start,
                'limit'         : limit
            })
            for event in events:
                yield event
            start += limit
            if len(events) < limit:
                break

###############################
##         Harmonia          ##
###############################

    def get_harmonia_artist(self, service_name=None, service_id=None):
        """Get an Artist from the Blitzr API with a external service ID.

        :param service_name: The service name
        :param service_id: The Artist's ID in the external service
        :type service_name: string
        :type service_id: string | int
        :return: Artist
        :rtype: dictionary

        """
        return self._request('harmonia/artist/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_release(self, service_name=None, service_id=None):
        """Get a Release from the Blitzr API with a external service ID.

        :param service_name: The service name
        :param service_id: The Release's ID in the external service
        :type service_name: string
        :type service_id: string | int
        :return: Release
        :rtype: dictionary

        """
        return self._request('harmonia/release/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_label(self, service_name=None, service_id=None):
        """Get a Label from the Blitzr API with a external service ID.

        :param service_name: The service name
        :param service_id: The Label's ID in the external service
        :type service_name: string
        :type service_id: string | int
        :return: Label
        :rtype: dictionary

        """
        return self._request('harmonia/label/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_search_by_source(self, source_name=None, source_id=None, source_filters=[],
                                      strict=False):
        """Get a Track from the Blitzr API with a external source ID.

        :param source_name: The source name
        :param source_id: The Track's ID in the external source
        :param source_filters: Filter the source
        :param strict: True if you want blitzr to guess the best result for you.
            False if you want all matched results
        :type source_name: string
        :type source_id: string | int
        :type source_filters: array
        :type strict: bool
        :return: Track
        :rtype: generator

        """
        for track in self._request('harmonia/searchbysource/', {
                'source_name'       : source_name,
                'source_id'         : source_id,
                'source_filters'    : ','.join(source_filters) if source_filters else None,
                'strict'            : 'true' if strict else 'false'
            }):
            yield track

###############################
##          Labels           ##
###############################

    def get_label(self, uuid=None, slug=None, extras=[], extras_limit=None):
        """Get a Label from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :param extras: Label extras : biography, websites, artists, last_releases, relations
        :param extras_limit: An int to set the limit of the lists fetched by extras.
        :type uuid: string
        :type slug: string
        :type extras: array
        :type extras_limit: int
        :return: Label
        :rtype: dictionary

        """
        return self._request('label/', {
            'uuid'         : uuid,
            'slug'         : slug,
            'extras'       : ','.join(extras) if extras else None,
            'extras_limit' : extras_limit
        })

    def get_label_artists(self, uuid=None, slug=None, start=0, limit=10):
        """Get a Label's artists from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :type uuid: string
        :type slug: string
        :return: Labels
        :rtype: generator

        """
        while True:
            artists = self._request('label/artists/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for artist in artists:
                yield artist
            start += limit
            if len(artists) < limit:
                break

    def get_label_biography(self, uuid=None, slug=None, html_format=False, url_scheme=None):
        """Get a Label's biography from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :param html_format: True for HTML markup in the biography
        :param url_scheme: Urlencoded links format
        :type uuid: string
        :type slug: string
        :type html_format: bool
        :type url_scheme: string
        :return: Biography
        :rtype: dictionary

        """
        return self._request('label/biography/', {
            'slug'       : slug,
            'uuid'       : uuid,
            'format'     : 'html' if html_format else None,
            'url_scheme' : url_scheme
        })

    def get_label_releases(self, uuid=None, slug=None, release_format=None, start=0, limit=10):
        """Get a Label's releases from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :param release_format: Release format (album|single|live|all)
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type start: int
        :type limit: int
        :type release_format: string
        :return: Releases
        :rtype: generator

        """
        while True:
            releases = self._request('label/releases/', {
                'uuid'      : uuid,
                'slug'      : slug,
                'format'    : release_format,
                'start'     : start,
                'limit'     : limit
            })
            for release in releases:
                yield release
            start += limit
            if len(releases) < limit:
                break

    def get_label_similar(self, uuid=None, slug=None, start=0, limit=10):
        """Get similar Labels from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :param filters: Filter results. Available filters : location
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type uuid: string
        :type slug: string
        :type filters: array
        :type start: int
        :type limit: int
        :return: Labels
        :rtype: generator

        """
        while True:
            labels = self._request('label/similars/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for label in labels:
                yield label
            start += limit
            if len(labels) < limit:
                break

    def get_label_websites(self, uuid=None, slug=None):
        """Get Label's websites from the Blitzr API.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :type uuid: string
        :type slug: string
        :return: Websites
        :rtype: generator

        """
        for website in self._request('label/websites/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield website

###############################
##          Radio            ##
###############################

    def get_radio_artist(self, uuid=None, slug=None, limit=10):
        """Get an Artist's Radio, a List of Track from the given Artist discography.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param limit: The number of Tracks needed
        :type uuid: string
        :type slug: string
        :type limit: int
        :return: Tracks
        :rtype: generator

        """
        for track in self._request('radio/artist/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'limit' : limit
            }):
            yield track

    def get_radio_artist_similar(self, uuid=None, slug=None, limit=10):
        """Get an Artist Similar Radio, a List of Track from the Similar Artist discography.

        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :param limit: The number of Tracks needed
        :type uuid: string
        :type slug: string
        :type limit: int
        :return: Tracks
        :rtype: generator

        """
        for track in self._request('radio/artist/similar/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'limit' : limit
            }):
            yield track

    def get_radio_label(self, uuid=None, slug=None, limit=10):
        """Get a Label's Radio, a List of Track from the given Label discography.

        :param uuid: The Label UUID
        :param slug: The Label Slug
        :param limit: The number of Tracks needed
        :type uuid: string
        :type slug: string
        :type limit: int
        :return: Tracks
        :rtype: generator

        """
        for track in self._request('radio/label/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'limit' : limit
            }):
            yield track

    def get_radio_tag(self, slug=None, limit=10):
        """Get a Tag Radio, a List of Track from the given Tag catalog.

        :param slug: The Tag Slug
        :param limit: The number of Tracks needed
        :type slug: string
        :type limit: int
        :return: Tracks
        :rtype: generator

        """
        for track in self._request('radio/tag/', {
                'slug'  : slug,
                'limit' : limit
            }):
            yield track

###############################
##         Releases          ##
###############################

    def get_release(self, uuid=None, slug=None):
        """Get a Release from the Blitzr API.

        :param uuid: The Release UUID
        :param slug: The Release Slug
        :type uuid: string
        :type slug: string
        :return: Release
        :rtype: dictionary

        """
        return self._request('release/', {
            'uuid'  : uuid,
            'slug'  : slug
        })

    def get_release_sources(self, uuid=None, slug=None):
        """Get the Release Ids for other Services. Slug or UUID are mandatory.

        :param uuid: The Release UUID
        :param slug: The Release Slug
        :type uuid: string
        :type slug: string
        :return: List of equivalence in other services
        :rtype: generator

        """
        for service in self._request('release/sources/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield service

###############################
##          Search           ##
###############################

    def search_artist(self, query=None, filters=[], autocomplete=False, start=0, limit=10,
                      extras=True):
        """Search Artist by query and filters.

        :param query: Your query
        :param filters: Filter results. Available filters : location, tag, type
        :param autocomplete: Enable predictive search
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :param extras: Get extra info like number of results
        :type query: string
        :type filters: array
        :type autocomplete: bool
        :type start: int
        :type limit: int
        :type extras: bool
        :return: Artists
        :rtype: generator

        """
        return SearchGenerator(self, 'search/artist/', query,
                               filters, autocomplete, start, limit, extras)

    def search_label(self, query=None, filters=[], autocomplete=False, start=0, limit=10,
                     extras=True):
        """Search Label by query and filters.

        :param query: Your query
        :param filters: Filter results. Available filters : location, tag
        :param autocomplete: Enable predictive search
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :param extras: Get extra info like number of results
        :type query: string
        :type filters: array
        :type autocomplete: bool
        :type start: int
        :type limit: int
        :type extras: bool
        :return: Labels
        :rtype: generator

        """
        return SearchGenerator(self, 'search/label/', query, filters,
                               autocomplete, start, limit, extras)

    def search_release(self, query=None, filters=[], autocomplete=False, start=0,
                       limit=10, extras=True):
        """Search Release by query and filters.

        :param query: Your query
        :param filters: Filter results. Available filters : artist, tag, format_summary,
            year, location
        :param autocomplete: Enable predictive search
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :param extras: Get extra info like number of results
        :type query: string
        :type filters: array
        :type autocomplete: bool
        :type start: int
        :type limit: int
        :type extras: bool
        :return: Releases
        :rtype: generator

        """
        return SearchGenerator(self, 'search/release/', query, filters,
                               autocomplete, start, limit, extras)

    def search_track(self, query=None, filters=[], start=0, limit=10, extras=True):
        """Search Track by query and filters.

        :param query: Your query
        :param filters: Filter results. Available filters : artist, release, format_summary,
            year, location
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :param extras: Get extra info like number of results
        :type query: string
        :type filters: array
        :type start: int
        :type limit: int
        :type extras: bool
        :return: Tracks
        :rtype: generator

        """
        return SearchGenerator(self, 'search/track/', query, filters,
                               None, start, limit, extras)

    def search_city(self, query=None, autocomplete=True, latitude=None, longitude=None,
                    start=0, limit=10):
        """Search City by query or geolocation.

        :param query: Your query
        :param autocomplete: Enable predictive search
        :param latitude: Latitude of the city
        :param longitude: Longitude of the city
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type query: string
        :type autocomplete: bool
        :type latitude: float
        :type longitude: float
        :type start: int
        :type limit: int
        :return: Cities
        :rtype: generator

        """
        while True:
            cities = self._request('search/city/', {
                'query'         : query,
                'autocomplete'  : 'true' if autocomplete else 'false',
                'latitude'      : latitude,
                'longitude'     : longitude,
                'start'         : start,
                'limit'         : limit
            })
            for city in cities:
                yield city
            start += limit
            if len(cities) < limit:
                break

    def search_country(self, country_code, start=0, limit=10):
        """Search Country by country code.

        :param country_code:  Official country code
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type country_code: string
        :type start: int
        :type limit: int
        :return: Countries
        :rtype: generator

        """
        while True:
            countries = self._request('search/country/', {
                'country_code'  : country_code,
                'start'         : start,
                'limit'         : limit
            })
            for country in countries:
                yield country
            start += limit
            if len(countries) < limit:
                break

###############################
##           Shop            ##
###############################

    def get_shop_artist(self, product_type, uuid=None, slug=None):
        """Get Artist's related products from the Blitzr API.

        :param product_type: The product's type (cd|lp|mp3|merch)
        :param uuid: The Artist UUID
        :param slug: The Artist Slug
        :type product_type: string
        :type uuid: string
        :type slug: string
        :return: Products
        :rtype: generator

        """
        for product in self._request('buy/artist/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_label(self, product_type, uuid=None, slug=None):
        """Get Label's related products from the Blitzr API.

        :param product_type: The product's type (cd|lp|merch)
        :param uuid: The Label UUID
        :param slug: The Label Slug
        :type product_type: string
        :type uuid: string
        :type slug: string
        :return: Products
        :rtype: generator

        """
        for product in self._request('buy/label/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_release(self, product_type, uuid=None, slug=None):
        """Get Release's related products from the Blitzr API.

        :param product_type: The product's type (cd|lp|mp3)
        :param uuid: The Release UUID
        :param slug: The Release Slug
        :type product_type: string
        :type uuid: string
        :type slug: string
        :return: Products
        :rtype: generator

        """
        for product in self._request('buy/release/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_track(self, uuid=None):
        """Get Track's related products from the Blitzr API.

        :param uuid: The Track UUID
        :type uuid: string
        :return: Products
        :rtype: generator

        """
        for product in self._request('buy/track/', {
                'uuid'  : uuid
            }):
            yield product

###############################
##            Tag            ##
###############################

    def get_tag(self, slug=None):
        """Get a Tag from the Blitzr API.

        :param slug: The Tag slug
        :type slug: string
        :return: Tag
        :rtype: dictionary

        """
        return self._request('tag/', {
            'slug'  : slug
        })

    def get_tag_artists(self, slug=None, start=0, limit=10):
        """Get Artists from a Tag

        :param slug: The Tag Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type slug: string
        :type start: int
        :type limit: int
        :return: Artists
        :rtype: generator

        """
        while True:
            artists = self._request('tag/artists/', {
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for artist in artists:
                yield artist
            start += limit
            if len(artists) < limit:
                break

    def get_tag_releases(self, slug=None, start=0, limit=10):
        """Get Releases from a Tag

        :param slug: The Tag Slug
        :param start: Offset for pagination
        :param limit: Size of generator batch
        :type slug: string
        :type start: int
        :type limit: int
        :return: Releases
        :rtype: generator

        """
        while True:
            releases = self._request('tag/releases/', {
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for release in releases:
                yield release
            start += limit
            if len(releases) < limit:
                break

###############################
##           Track           ##
###############################

    def get_track(self, uuid=None):
        """Get a Track from the Blitzr API.

        :param uuid: The Track UUID
        :type uuid: string
        :return: Track
        :rtype: dictionary

        """
        return self._request('track/', {
            'uuid'  : uuid
        })

    def get_track_sources(self, uuid=None):
        """Get a Track's Sources from the Blitzr API.

        :param uuid: The Track UUID
        :type uuid: string
        :return: Source
        :rtype: generator

        """
        for source in self._request('track/sources/', {
                'uuid'  : uuid
            }):
            yield source


###############################
##     Search Generators     ##
###############################

class SearchGenerator(object):
    """Custom Generator for Search requests, provides length compatibility.

    The only non standard generators are those returned by the search queries.
    They are differents by their ability to retreive the total count of elements
    to generate.

    If the field **extras** of your request is set to True, which is the default state,
    you will be able to call the **len()** method on the generator.

    :Example:

    >>> from blitzr import client
    >>> blitzr = client.BlitzrClient(your_api_key)
    >>> artists = blitzr.search_artist(query='emine', autocomplete=True)
    >>> print len(artists)
    80

    Then it works exactly as all other generators.

    :Example:

    >>> for artist in artists:
    >>>     print artist.get('name')
    Emine
    Emine
    Eminem
    Emine Krasniqi
    Eminence
    Eminent
    Eminent
    ...

    """
    def __init__(self, client=None, endpoint=None, query=None, filters=[],
                 autocomplete=True, start=0, limit=10, extras=False):
        self.client = client
        self.endpoint = endpoint
        self.query = query
        self.filters = filters
        self.autocomplete = autocomplete
        self.start = start
        self.limit = limit
        self.extras = extras
        self.cursor = -1
        self.results = None
        self._length = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """Get next result."""
        self.cursor += 1
        if self.results is None or self.cursor == self.limit:
            self._request()
            self.cursor = 0

        if self.cursor < len(self.results):
            return self.results[self.cursor]
        else:
            raise StopIteration()

    def _request(self):
        answer = self.client._request(self.endpoint, {
            'query'         : self.query,
            'filters'       : ','.join(self.filters) if self.filters else None,
            'autocomplete'  : 'true' if self.autocomplete else 'false',
            'start'         : self.start,
            'limit'         : self.limit,
            'extras'        : 'true' if self.extras else 'false'
        })
        self.start += self.limit
        if self.extras:
            self.results = answer.get('results')
            self._length = answer.get('total')
        else:
            self.results = answer

    def __len__(self):
        "This method returns the total number of elements"
        if self._length or self._length == 0:
            return self._length
        elif self.extras:
            self._request()
            return self._length
        else:
            raise ConfigurationException('The extra parameter has been set to False, ' +
                                         'you don\'t have access to the length of the results.')

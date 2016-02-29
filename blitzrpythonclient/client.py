import requests
from .exceptions import (ConfigurationException, ServerException, ClientException, NetworkException)

class BlitzrClient(object):

    BASE_URL = "https://api.blitzr.com/"

    def __init__(self, api_key):
        if api_key:
            self.api_key = api_key
        else:
            raise ConfigurationException('api_key is missing.')

    def _request(self, method, params):
        url = self.BASE_URL + method
        params['key'] = self.api_key
        try:
            req = requests.get(url=url, params=params)
            req.raise_for_status()
            return req.json()
        except requests.exceptions.HTTPError:
            if req.status_code >= 500:
                raise ServerException('An error occured on the Blitzr side. HTTP code: ' + str(req.status_code))
            elif req.status_code >= 400:
                raise ClientException(req.json())
        except requests.exceptions.ConnectionError as exception:
            raise NetworkException(str(exception))


###############################
##          Artists          ##
###############################


    def get_artist(self, uuid=None, slug=None, extras=[], extras_limit=None):
        return self._request('artist/', {
            'uuid'         : uuid,
            'slug'         : slug,
            'extras'       : ','.join(extras) if extras else None,
            'extras_limit' : extras_limit
        })

    def get_artist_aliases(self, uuid=None, slug=None):
        for alias in self._request('artist/aliases/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield alias

    def get_artist_bands(self, uuid=None, slug=None, start=0, limit=10):
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

    def get_artist_biography(self, uuid=None, slug=None, lang=None, html_format=False, url_scheme=None):
        return self._request('artist/biography/', {
            'slug'       : slug,
            'uuid'       : uuid,
            'lang'       : lang,
            'format'     : 'html' if html_format else None,
            'url_scheme' : url_scheme
        })

    def get_artist_events(self, uuid=None, slug=None, start=0, limit=10):
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

    def get_artist_releases(self, uuid=None, slug=None, start=0, limit=10, release_type=None, release_format=None, credited=False):
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

    def get_artist_similar(self, uuid=None, slug=None, start=0, limit=10):
        while True:
            similar = self._request('artist/similars/', {
                'uuid'  : uuid,
                'slug'  : slug,
                'start' : start,
                'limit' : limit
            })
            for artist in similar:
                yield artist
            start += limit
            if len(similar) < limit:
                break

    def get_artist_summary(self, uuid=None, slug=None):
        return self._request('artist/summary/', {
            'uuid'  : uuid,
            'slug'  : slug,
        })

    def get_artist_websites(self, uuid=None, slug=None):
        for website in self._request('artist/websites/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield website


###############################
##           Events          ##
###############################

    def get_event(self, uuid=None, slug=None):
        return self._request('event/', {
            'uuid'  : uuid,
            'slug'  : slug,
        })

    def get_events(self, country_code=None, latitude=None, longitude=None, city=None, venue=None, tag=None, date_start=None, date_end=None, radius=None, start=0, limit=10):
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
        return self._request('harmonia/artist/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_release(self, service_name=None, service_id=None):
        return self._request('harmonia/release/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_label(self, service_name=None, service_id=None):
        return self._request('harmonia/label/', {
            'service_name'  : service_name,
            'service_id'    : service_id,
        })

    def get_harmonia_search_by_source(self, source_name=None, source_id=None, source_filters=[], strict=False):
        return self._request('harmonia/searchbysource/', {
            'source_name'       : source_name,
            'source_id'         : source_id,
            'source_filters'    : ','.join(source_filters) if source_filters else None,
            'strict'            : 'true' if strict else 'false'
        })

###############################
##          Labels           ##
###############################

    def get_label(self, uuid=None, slug=None, extras=[], extras_limit=None):
        return self._request('label/', {
            'uuid'         : uuid,
            'slug'         : slug,
            'extras'       : ','.join(extras) if extras else None,
            'extras_limit' : extras_limit
        })

    def get_label_artists(self, uuid=None, slug=None, start=0, limit=10):
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
        return self._request('label/biography/', {
            'slug'       : slug,
            'uuid'       : uuid,
            'format'     : 'html' if html_format else None,
            'url_scheme' : url_scheme
        })

    def get_label_releases(self, uuid=None, slug=None, release_format=None, start=0, limit=10):
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
        for website in self._request('label/websites/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield website

###############################
##         Releases          ##
###############################

    def get_release(self, uuid=None, slug=None):
        return self._request('release/', {
            'uuid'  : uuid,
            'slug'  : slug
        })

    def get_release_sources(self, uuid=None, slug=None):
        for track in self._request('release/sources/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield track

###############################
##          Search           ##
###############################

    def search_artist(self, query=None, filters=[], autocomplete=True, start=0, limit=10, extras=False):
        while True:
            artists = self._request('search/artist/', {
                'query'         : query,
                'filters'       : ','.join(filters) if filters else None,
                'autocomplete'  : 'true' if autocomplete else 'false',
                'start'         : start,
                'limit'         : limit,
                'extras'        : 'true' if extras else 'false'
            })
            for artist in artists:
                yield artist
            start += limit
            if len(artists) < limit:
                break

    def search_label(self, query=None, filters=[], autocomplete=True, start=0, limit=10, extras=False):
        while True:
            labels = self._request('search/label/', {
                'query'         : query,
                'filters'       : ','.join(filters) if filters else None,
                'autocomplete'  : 'true' if autocomplete else 'false',
                'start'         : start,
                'limit'         : limit,
                'extras'        : 'true' if extras else 'false'
            })
            for label in labels:
                yield label
            start += limit
            if len(labels) < limit:
                break

    def search_release(self, query=None, filters=[], autocomplete=True, start=0, limit=10, extras=False):
        while True:
            releases = self._request('search/release/', {
                'query'         : query,
                'filters'       : ','.join(filters) if filters else None,
                'autocomplete'  : 'true' if autocomplete else 'false',
                'start'         : start,
                'limit'         : limit,
                'extras'        : 'true' if extras else 'false'
            })
            for release in releases:
                yield release
            start += limit
            if len(releases) < limit:
                break

    def search_track(self, query=None, filters=[], start=0, limit=10, extras=False):
        while True:
            tracks = self._request('search/track/', {
                'query'     : query,
                'filters'   : ','.join(filters) if filters else None,
                'start'     : start,
                'limit'     : limit,
                'extras'    : 'true' if extras else 'false'
            })
            for track in tracks:
                yield track
            start += limit
            if len(tracks) < limit:
                break

    def search_city(self, query=None, autocomplete=True, latitude=None, longitude=None, start=0, limit=10):
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
        for product in self._request('buy/artist/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_label(self, product_type, uuid=None, slug=None):
        for product in self._request('buy/label/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_release(self, product_type, uuid=None, slug=None):
        for product in self._request('buy/release/' + product_type + '/', {
                'uuid'  : uuid,
                'slug'  : slug
            }):
            yield product

    def get_shop_track(self, uuid=None):
        for product in self._request('buy/track/', {
                'uuid'  : uuid
            }):
            yield product

###############################
##            Tag            ##
###############################

    def get_tag(self, slug=None):
        return self._request('tag/', {
            'slug'  : slug
        })

    def get_tag_artists(self, slug=None, start=0, limit=10):
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
        return self._request('track/', {
            'uuid'  : uuid
        })

    def get_track_sources(self, uuid=None):
        for source in self._request('track/sources/', {
                'uuid'  : uuid
            }):
            yield source

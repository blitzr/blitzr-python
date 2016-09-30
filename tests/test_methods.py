import unittest

from mock import patch

from blitzr import BlitzrClient


API_KEY = 'testing'

class TestBlitzrClient(unittest.TestCase):

    @patch('requests.get')
    def test_request_simple(self, mock_method):
        BlitzrClient(API_KEY)._request(method='/toto', params={})
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + '/toto', params={'key': API_KEY})

    @patch('requests.get')
    def test_request_with_params(self, mock_method):
        BlitzrClient(API_KEY)._request(method='/toto', params={'toto': 'toto'})
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + '/toto', params={'key': API_KEY, 'toto': 'toto'})

    @patch('requests.get')
    def test_get_artist_by_slug(self, mock_method):
        BlitzrClient(API_KEY).get_artist(slug='toto')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + 'artist/', params={'key': API_KEY, 'slug':'toto', 'uuid':None, 'extras':None, 'extras_limit':None})

    @patch('requests.get')
    def test_get_artist_by_uuid(self, mock_method):
        BlitzrClient(API_KEY).get_artist(uuid='AR89798789798787')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + 'artist/', params={'key': API_KEY, 'slug':None, 'uuid':'AR89798789798787', 'extras':None, 'extras_limit':None})

    @patch('requests.get')
    def test_get_artist_aliases_by_slug(self, mock_method):
        BlitzrClient(API_KEY).get_artist_aliases(slug='toto')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + 'artist/aliases/', params={'key': API_KEY, 'slug':'toto', 'uuid':None})

    @patch('requests.get')
    def test_get_artist_aliases_by_uuid(self, mock_method):
        BlitzrClient(API_KEY).get_artist_aliases(uuid='AR89798789798787')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL + 'artist/aliases/', params={'key': API_KEY, 'slug':None, 'uuid':'AR89798789798787'})

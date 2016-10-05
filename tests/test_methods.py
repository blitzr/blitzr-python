import unittest

from mock import patch

import types

from blitzr import BlitzrClient


API_KEY = 'testing'

class TestBlitzrClient(unittest.TestCase):

    @patch('requests.get')
    def test_request_simple(self, mock_method):
        BlitzrClient(API_KEY)._request(method='/blitzr_method')
        mock_method.assert_called_once_with(
            url=BlitzrClient.BASE_URL % '/blitzr_method',
            params={
                'key'   : API_KEY
            }
        )

    @patch('requests.get')
    def test_request_with_params(self, mock_method):
        BlitzrClient(API_KEY)._request(method='/blitzr_method', params={'toto': 'toto'})
        mock_method.assert_called_once_with(
            url=BlitzrClient.BASE_URL % '/blitzr_method',
            params={
                'key'   : API_KEY,
                'toto'  : 'toto'
            }
        )

    @patch('requests.get')
    def test_all_methods(self, mock_method):
        blitzr_client = BlitzrClient(API_KEY)
        for m in dir(BlitzrClient):
            mf = BlitzrClient.__dict__.get(m)
            if isinstance(mf, types.FunctionType) and m[0] != '_':
                print(m)
                with self.subTest(i=m):
                    mf(blitzr_client, None)
                    mock_method.assert_called()


    @patch('requests.get')
    def test_get_artist_by_slug(self, mock_method):

        BlitzrClient(API_KEY).get_artist(slug='toto')
        mock_method.assert_called_once_with(
            url=BlitzrClient.BASE_URL % '/artist/',
            params={
                'key'           : API_KEY,
                'slug'          : 'toto',
                'uuid'          : None,
                'extras'        : None,
                'extras_limit'  : None
            }
        )

    @patch('requests.get')
    def test_get_artist_by_uuid(self, mock_method):
        BlitzrClient(API_KEY).get_artist(uuid='AR89798789798787')
        mock_method.assert_called_once_with(
            url=BlitzrClient.BASE_URL % '/artist/',
            params={
                'key'           : API_KEY,
                'slug'          : None,
                'uuid'          : 'AR89798789798787',
                'extras'        : None,
                'extras_limit'  : None
            })

    @patch('requests.get')
    def test_get_artist_aliases_by_slug(self, mock_method):
        BlitzrClient(API_KEY).get_artist_aliases(slug='toto')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL % '/artist/aliases/', params={'key': API_KEY, 'slug':'toto', 'uuid':None})

    @patch('requests.get')
    def test_get_artist_aliases_by_uuid(self, mock_method):
        BlitzrClient(API_KEY).get_artist_aliases(uuid='AR89798789798787')
        mock_method.assert_called_once_with(url=BlitzrClient.BASE_URL % '/artist/aliases/', params={'key': API_KEY, 'slug':None, 'uuid':'AR89798789798787'})

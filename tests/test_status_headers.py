import json
import unittest

from crawlbase.base_api import BaseAPI


class FakeHeaders(dict):
    """Minimal header map supporting both `in` and `.get` like HTTPMessage."""

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default


class FakeHandler(object):
    def __init__(self, headers):
        self.headers = headers


class BaseAPIStatusTestCase(unittest.TestCase):
    def setUp(self):
        self.api = BaseAPI({'token': 'test-token'})
        self.api.response = {'headers': {}, 'body': ''}

    def _parse_regular(self, headers):
        self.api.response = {'headers': {}, 'body': ''}
        self.api.parseRegularResponse(FakeHandler(FakeHeaders(headers)))
        return self.api.response['headers']

    def _parse_json(self, payload):
        self.api.response = {
            'headers': {},
            'body': json.dumps(payload),
        }
        self.api.parseJsonResponse()
        return self.api.response['headers']

    def test_resolve_only_cb_status(self):
        self.assertEqual(self.api._resolve_status({'cb_status': '200'}), '200')

    def test_resolve_only_pc_status(self):
        self.assertEqual(self.api._resolve_status({'pc_status': '200'}), '200')

    def test_resolve_both_prefers_cb_status(self):
        self.assertEqual(
            self.api._resolve_status({'cb_status': '200', 'pc_status': '503'}),
            '200',
        )

    def test_resolve_neither(self):
        self.assertIsNone(self.api._resolve_status({}))

    def test_resolve_empty_string_does_not_fall_back(self):
        self.assertEqual(
            self.api._resolve_status({'cb_status': '', 'pc_status': '200'}),
            '',
        )

    def test_regular_only_cb_status(self):
        headers = self._parse_regular({'cb_status': '200', 'original_status': '200', 'url': 'https://example.com'})
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_regular_only_pc_status(self):
        headers = self._parse_regular({'pc_status': '200', 'original_status': '200', 'url': 'https://example.com'})
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_regular_both_prefers_cb_status(self):
        headers = self._parse_regular({
            'cb_status': '200',
            'pc_status': '503',
            'original_status': '200',
            'url': 'https://example.com',
        })
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_regular_neither_status_header(self):
        headers = self._parse_regular({'original_status': '200', 'url': 'https://example.com'})
        self.assertEqual(headers['cb_status'], 'None')
        self.assertEqual(headers['pc_status'], 'None')

    def test_json_only_cb_status(self):
        headers = self._parse_json({
            'original_status': '200',
            'cb_status': '200',
            'url': 'https://example.com',
            'body': '<html></html>',
        })
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_json_only_pc_status(self):
        headers = self._parse_json({
            'original_status': '200',
            'pc_status': '200',
            'url': 'https://example.com',
            'body': '<html></html>',
        })
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_json_both_prefers_cb_status(self):
        headers = self._parse_json({
            'original_status': '200',
            'cb_status': '200',
            'pc_status': '503',
            'url': 'https://example.com',
            'body': '<html></html>',
        })
        self.assertEqual(headers['cb_status'], '200')
        self.assertEqual(headers['pc_status'], '200')

    def test_json_neither_status_field(self):
        headers = self._parse_json({
            'original_status': '200',
            'url': 'https://example.com',
            'body': '<html></html>',
        })
        self.assertEqual(headers['cb_status'], 'None')
        self.assertEqual(headers['pc_status'], 'None')

    def test_existing_pc_status_access_still_works(self):
        for headers in (
            self._parse_regular({'cb_status': '201'}),
            self._parse_regular({'pc_status': '202'}),
            self._parse_regular({'cb_status': '200', 'pc_status': '503'}),
        ):
            self.assertIn('pc_status', headers)
            self.assertTrue(headers['pc_status'])


if __name__ == '__main__':
    unittest.main()

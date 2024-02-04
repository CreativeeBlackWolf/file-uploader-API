import unittest

import requests

BASE_URL = "http://localhost:2727"


class TestConnection(unittest.TestCase):
    def test_connection(self):
        """Checks if the connection to the API server is working"""
        conn = requests.get(BASE_URL)

        self.assertEqual(conn.status_code, 404)

    def test_files_list_connection(self):
        """Checks if the connection to files list API is working"""
        conn = requests.get(BASE_URL + "/api/files/")
        self.assertEqual(conn.status_code, 200)

        wrong_conn = requests.post(BASE_URL + "/api/files/")
        self.assertEqual(wrong_conn.status_code, 405)

    def test_upload_connection(self):
        """Checks if the connection to API is working"""
        conn = requests.post(BASE_URL + "/api/upload/", data={"files": "lol"})

        self.assertEqual(conn.status_code, 400)
        self.assertDictEqual(
            conn.json(),
            {
                "files": "This field is required or files we're not uploaded via form-body"
            },
        )

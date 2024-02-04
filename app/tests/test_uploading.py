import os
import time
import unittest

import requests

BASE_URL = "http://localhost:2727"
FILES_DIR = os.path.dirname(os.path.abspath(__file__)) + "/files/"


class TestUploadingAPI(unittest.TestCase):
    def test_txt_upload(self):
        files = {"files": open(FILES_DIR + "test.txt")}
        r = requests.post(BASE_URL + "/api/upload/", files=files)

        print(r.json())
        on_upload_file_data = r.json()["files"][0]
        file_id = on_upload_file_data["id"]

        self.assertEqual(r.status_code, 201)
        self.assertEqual(on_upload_file_data["processed"], False)
        self.assertEqual(on_upload_file_data["data"], {})

        # Testing after uploading
        time.sleep(0.5)
        r = requests.get(BASE_URL + f"/api/files/{file_id}/")
        self.assertEqual(r.status_code, 200)

        handled_file_data = r.json()["data"]
        self.assertNotEqual(handled_file_data, {})
        self.assertEqual(handled_file_data["size"], "0.0 MB")
        self.assertIn("test", handled_file_data["filename"])
        self.assertEqual(handled_file_data["extension"], ".txt")

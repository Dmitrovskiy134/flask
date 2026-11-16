"""Автоматические проверки домашнего задания: python -m unittest -v."""
import tempfile
import unittest
from pathlib import Path

import app as ads_app


class AdsApiTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        ads_app.DB_PATH = Path(self.tmpdir.name) / "test.db"
        ads_app.init_db()
        self.client = ads_app.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_create_and_read(self):
        response = self.client.post("/ads", json={
            "title": "Ремонт холодильников",
            "description": "Выезд на дом",
            "owner": "Денис",
        })
        self.assertEqual(response.status_code, 201)
        ad = response.get_json()
        self.assertEqual(ad["id"], 1)
        self.assertEqual(ad["owner"], "Денис")
        self.assertIn("created_at", ad)
        self.assertEqual(self.client.get("/ads/1").get_json(), ad)
        self.assertEqual(len(self.client.get("/ads").get_json()), 1)

    def test_patch_and_delete(self):
        self.client.post("/ads", json={
            "title": "Ремонт", "description": "Услуги", "owner": "Денис"
        })
        response = self.client.patch("/ads/1", json={"title": "Ремонт кондиционеров"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Ремонт кондиционеров")
        self.assertEqual(response.get_json()["description"], "Услуги")
        self.assertEqual(self.client.delete("/ads/1").status_code, 204)
        self.assertEqual(self.client.get("/ads/1").status_code, 404)
        self.assertEqual(self.client.delete("/ads/1").status_code, 404)

    def test_validation(self):
        self.assertEqual(self.client.post("/ads", json={"title": "Только заголовок"}).status_code, 400)
        self.assertEqual(self.client.post("/ads", json=[1, 2]).status_code, 400)
        self.assertEqual(self.client.patch("/ads/99", json={"title": "Новое"}).status_code, 404)
        self.assertEqual(self.client.patch("/ads/99", json={"owner": "Чужой"}).status_code, 400)


if __name__ == "__main__":
    unittest.main()

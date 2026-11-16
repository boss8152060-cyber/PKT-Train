"""Checks that this repository is a valid module of PK Transport: manifest, plugin file, version bookkeeping."""
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def manifest():
    with open(os.path.join(ROOT, "pkt_module.json"), encoding="utf-8") as f:
        return json.load(f)


class Manifest(unittest.TestCase):
    def test_fields(self):
        m = manifest()
        self.assertEqual((m["api"], m["id"], m["name"]), (1, "train", "PKT Train"))
        self.assertRegex(m["version"], r"^\d+\.\d+\.\d+$")
        self.assertRegex(m["min_shell"], r"^\d+\.\d+\.\d+$")
        self.assertTrue(os.path.isfile(os.path.join(ROOT, m["plugin"])))
        self.assertTrue(os.path.isfile(os.path.join(ROOT, m["requirements_file"])))

    def test_the_version_is_the_one_of_the_changelog(self):
        log = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
        rows = re.findall(r"(?m)^\| \*\*(\d+\.\d+\.\d+)\*\* \|", log)
        self.assertEqual(manifest()["version"], rows[-1])

    def test_the_plugin_file_has_the_api(self):
        src = open(os.path.join(ROOT, "pkt_plugin.py"), encoding="utf-8").read()
        self.assertRegex(src, r"(?m)^API = 1$")
        for fn in ("create", "summary", "recent", "texts"):
            self.assertRegex(src, rf"(?m)^def {fn}\(", fn)
        top = src.split("\n\nAPI = 1")[0] if "\n\nAPI = 1" in src else src
        heavy = re.findall(r"(?m)^(?:import|from)\s+(torch|ultralytics|cv2|numpy|matplotlib)\b", src)
        self.assertEqual(heavy, [], "pkt_plugin.py must stay light at the top (PK Transport imports it on its Home page)")


class Package(unittest.TestCase):
    def test_the_package_imports_without_the_shell(self):
        import importlib
        for name in ("pkt_train.core", "pkt_train.runs", "pkt_train.texts"):
            importlib.import_module(name)
        from pkt_train.texts import TEXTS
        self.assertEqual(set(TEXTS["th"]), set(TEXTS["en"]))
        for lang in TEXTS.values():
            for key, text in lang.items():
                self.assertTrue(text.strip(), key)


if __name__ == "__main__":
    unittest.main()

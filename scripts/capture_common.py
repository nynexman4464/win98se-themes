"""Shared paths and inputs for the two Win98-native capture builders."""
from pathlib import Path
import hashlib,json
ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
HOST = "10.0.2.2"  # 86Box SLiRP host alias
PREVIEW_PORT = 8001
SHOWCASE_PORT = 8003
OUTPUT_PREVIEW = BUILD / "capture-preview.exe"
SCHEME_ORDER = ('brick', 'maple', 'spruce', 'teal-vga', 'red-white-and-blue-vga', 'wheat', 'pumpkin-large', 'eggplant', 'rainy-day', 'desert', 'marine-high-color', 'windows-standard-extra-large', 'storm-vga', 'windows-standard', 'windows-standard-large', 'rose', 'high-contrast-black-large', 'high-contrast-black-extra-large', 'high-contrast-white-large', 'high-contrast-white-extra-large', 'rose-large', 'lilac', 'lilac-large', 'slate', 'plum-high-color', 'high-contrast-black', 'high-contrast-white', 'high-contrast-1', 'high-contrast-1-large', 'high-contrast-1-extra-large', 'high-contrast-2', 'high-contrast-2-large', 'high-contrast-2-extra-large', 'windows-standard-default')

def load_schemes():
    schemes=[]
    for slug in SCHEME_ORDER:
        item=json.loads((ROOT / "themes" / (slug + ".json")).read_text(encoding="utf-8"))
        payload=bytes.fromhex(item["rawHex"])
        if len(payload)!=520 or hashlib.sha256(payload).hexdigest()!=item["sha256"]:
            raise ValueError("Invalid scheme payload: " + slug)
        schemes.append(item)
    if len(schemes)!=34:
        raise ValueError("The native capture loops expect this collection's 34 schemes")
    return schemes

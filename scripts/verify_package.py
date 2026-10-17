#!/usr/bin/env python3
"""Offline package self-check (stdlib only)."""
from pathlib import Path
from zipfile import ZipFile
import re, hashlib
root=Path(__file__).resolve().parents[1]
page=(root/'index.html').read_text(encoding='utf-8')
required=[
    'SUMI · 墨流し v0.3.0', 'class GPUFluid', 'class InkSurface',
    'currentTool', 'data-tool="water"', 'WATER_TOKEN',
    'uMode', 'SUMI_DIAGNOSTICS', "version:'0.3.0'",
]
for item in required:
    assert item in page, f'Missing expected app feature: {item}'
assert page.count('class GPUFluid')==1, 'GPUFluid must be declared once'
assert page.count('class InkSurface')==1, 'InkSurface must be declared once'
assert page.count("(()=>{'use strict';")==1, 'App boot IIFE must occur exactly once'
assert page.count('</script>')==1, 'Expected one self-contained script'
assert 'https://cdn.' not in page.lower(), 'Unexpected external script dependency'
assert "versionName '0.3.0'" in (root/'android/app/build.gradle').read_text()
assert "include 'index.html'" in (root/'android/app/build.gradle').read_text()
assert (root/'releases/SUMI-Suminagashi-v0.3.0.apk').is_file()
with ZipFile(root/'releases/SUMI-Suminagashi-v0.3.0.apk') as z:
    assert 'assets/index.html' in z.namelist(), 'APK missing HTML asset'
    old=z.read('assets/index.html')
    assert old==page.encode(), 'APK web asset differs from root index.html'
print('PACKAGE OK — single HTML source, version, water mode, APK parity')
print('SHA256(index.html):',hashlib.sha256(page.encode()).hexdigest())

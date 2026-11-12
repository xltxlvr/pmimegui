# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pmimegui.py'],
    pathex=[],
    binaries=[],
    datas=[('pmimegui.png', '.'), ('kyujitai.json', '.'), ('shinjitai.json', '.'), ('simplified.json', '.'), ('customkanji.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pm IME GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['pmimegui.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pm IME GUI',
)
app = BUNDLE(
    coll,
    name='pm IME GUI.app',
    icon='pmimegui.icns',
    bundle_identifier=None,
)

# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['kokoshare_filetransfer.py'],
    pathex=[],
    binaries=[],
    datas=[('app_icon.png', '.')],  # This is correct.
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
    pyz,  # pyz should come first as it's positional
    a.scripts,
    a.binaries,
    a.datas,
    [],
    metadata=("KokoShare File Transfer", "File Transfer Application", "KokoDocs", "1.1.2", "Publisher: Rizko Imsar"),
    name='kokoshare_filetransfer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # icon should now be the keyword argument
)
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['kokoshare_filetransfer.py'],
    pathex=[],
    binaries=[],
    datas=[('app_icon.png', '.')],  # This is correct.
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
    pyz,  # pyz should come first as it's positional
    a.scripts,
    a.binaries,
    a.datas,
    [],
    metadata=("KokoShare File Transfer", "File Transfer Application", "KokoDocs", "1.1.2", "Publisher: Rizko Imsar"),
    name='kokoshare_filetransfer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # icon should now be the keyword argument
)

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files=[
    ('LICENSE.txt', '.'),
    ('config_default/', 'config_default/'),
    ('clueReport.pdf', '.'),
    ('radio.ico','.'),
    ('rotateCsvBackups.ps1','.'),
    ('icons/user_icon_80px.png','icons')
]

a = Analysis(
    ['radiolog.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='radiolog',
    icon='radio.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.' # see https://github.com/ncssar/radiolog/issues/695#issuecomment-1807152764
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='radiolog',
)

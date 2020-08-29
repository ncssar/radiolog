# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['radiolog.py'],
             pathex=['.', '..\\gwpycore', '.venv\\Lib\\site-packages'],
             binaries=[],
             datas= [ ('app\\ui\\*.ui', 'app\\ui' ),
             ( 'local_default', 'local_default'),
             ( 'assets', 'assets'),
             ( 'radiolog_ui_rc.py', '.' ) ],
             hiddenimports=["pyproj.datadir","pywintypes","QLineEditWithDeselect"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='radiolog',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='radiolog')

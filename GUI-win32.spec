# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

import kivymd
from os.path import dirname, abspath, join, basename

uix = os.path.join(kivymd.path, f"uix{os.sep}")
toast = os.path.join(kivymd.path, f"toast{os.sep}")

a = Analysis(['decentra_network\\gui\\main.py'],
             pathex=[],
             binaries=[],
             datas=[
                (uix, join("kivymd", basename(dirname(uix)))),
                (toast, join("kivymd", basename(dirname(toast)))),
             ],
             hiddenimports=["kivymd_extensions","kivymd_extensions.sweetalert", "sqlite3", "qrcode", "qrcode.image.styledpil", "qrcode.image.styles.colormasks", "plyer"],
             hookspath=[kivymd_hooks_path],
             hooksconfig={},
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
          name='Decentra-Network-GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Decentra-Network-GUI')

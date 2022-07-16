# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

import kivymd
from os.path import dirname, abspath, join, basename

stiffscroll = os.path.join(kivymd.path, f"stiffscroll{os.sep}")

a = Analysis(['decentra_network\\gui.py'],
             pathex=[],
             binaries=[],
             datas=[(stiffscroll, join("kivymd", basename(dirname(stiffscroll)))),],
             hiddenimports=["kivymd_extensions","kivymd_extensions.sweetalert"],
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

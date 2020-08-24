# -*- mode: python -*-

block_cipher = None

from app import __version__, __appname__, __desktopid__, __description__

a = Analysis(['bin/app'],
             pathex=['.'],
             binaries=None,
             datas=[],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='app',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources\\icons\\app.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=__appname__)

app = BUNDLE(coll,
             name='{}.app'.format(__appname__),
             icon='resources/icons/app.icns',
             bundle_identifier=__desktopid__,
             info_plist={
                'CFBundleName': __appname__,
                'CFBundleVersion': __version__,
                'CFBundleShortVersionString': __version__,
                'NSPrincipalClass': 'NSApplication',
                'NSHighResolutionCapable': 'True'
                }
             )

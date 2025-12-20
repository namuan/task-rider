# -*- mode: python -*-

block_cipher = None

import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))

from app import __version__, __appname__, __desktopid__, __description__
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules("dataset")
hiddenimports += collect_submodules("pyremindkit")

a = Analysis(['bin/app'],
             pathex=['.'],
             binaries=None,
             datas=[
                ('resources/images/*', 'resources/images'),
                ('resources/icons/*', 'resources/icons'),
                ('resources/fonts/*', 'resources/fonts'),
                ('resources/themes/*', 'resources/themes'),
                ('resources/sounds/*', 'resources/sounds'),
             ],
             hiddenimports=hiddenimports,
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
          entitlements_file='entitlements.plist',
          icon='assets/icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=__appname__)

app = BUNDLE(coll,
             name='{}.app'.format(__appname__),
             icon='assets/icon.icns',
             bundle_identifier=__desktopid__,
             info_plist={
                'CFBundleName': __appname__,
                'CFBundleVersion': __version__,
                'CFBundleShortVersionString': __version__,
                'NSPrincipalClass': 'NSApplication',
                'NSHighResolutionCapable': 'True',
                'NSRemindersUsageDescription': 'Task Rider needs access to Reminders to sync tasks.',
                'NSCalendarsUsageDescription': 'Task Rider needs access to Calendars to sync tasks.'
                }
             )

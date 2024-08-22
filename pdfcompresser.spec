# pdfcompresser.spec
import sys
from PyInstaller.utils.hooks import copy_metadata

a = Analysis(
    ['p.py'],
    pathex=['.'],
    binaries=[('gs/gswin64c.exe', 'gs')],
    datas=[('images/logo.png', 'images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Small PDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Ensure no console window appears
    icon='images/logo.ico',  # Set the icon for the executable
)

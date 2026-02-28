a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('settings.py', '.'),      # Файл : Куди покласти в EXE
        ('assets', 'assets'),      # Папка : Куди покласти в EXE
        ('src', 'src'),            # Твій код у папках
        ('levels', 'levels'),

    ],
    hiddenimports=[],
    tmpdir=None,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Platformer',           # Назва твого .exe
    debug=False,
    strip=False,
    upx=True,
    console=True,             # Постав False, щоб прибрати консоль
    contents_directory='.',   # Важливо для нових версій PyInstaller
)
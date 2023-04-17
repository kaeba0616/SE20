/*** 아래의 .spec 파일을 참고
**** pathex 변수에 'C:\\Users\\user\\Desktop\\SE20\\unogame' 입력
**** datas 변수에 파일(e.g. mp3파일, ttf파일, png파일 등)을 ***경로에 맞게*** 입력
**** hiddenimports 변수에 사용하는 모듈(e.g. utils.menu 등)을 ***전부*** 입력
**** 처음 .spec 파일도 뭣도 아무것도 없는 상태면 pyinstaller --onefile --noconsole main.py 사용하면
**** dist, build 폴더랑 main.spec 파일이 생성이 됨
**** exe 파일은 dist 폴더 안에 생성됨
**** .spec파일을 위에 말한대로 조작 한 후
**** pyinstaller main.spec을 하면 조작한대로 exe 파일이 다시 생성이 됨
**** 근데... 경로가 좀 이상해서 dist 안에서 exe 파일을 unogame으로 꺼내야 실행이 됨
**** 나중에 실행 할 때는 바탕화면으로 바로가기 만들기 해서 실행하는걸 권장함
***/

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\user\\Desktop\\SE20\\unogame'],
    binaries=[],
    datas=[('./resources/fonts/Pixeltype.ttf', './resources/fonts'),
('./resources/music/*.mp3', './resources/music'),
('./resources/sounds/*.mp3', './resources/sounds'),
('./resources/images/*.png', './resources/images'),
('./resources/images/*.png', './resources/images')],
    hiddenimports=[
    'os',
    'utils.__init__',
    'utils.menu',
    'utils.storyMode',
    'utils.settings',
    'utils.sound',
    'single_play',
    'models.__init__',
    'models.AI',
    'models.button',
    'models.card',
    'models.deck',
    'models.Human',
    'models.player',
    'models.stage'
],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)

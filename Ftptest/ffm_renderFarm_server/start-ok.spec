# -*- mode: python -*-

block_cipher = None


a = Analysis(['start.py'],
             pathex=['D:\\FFM\\code\\ffm_renderFarm_server'],
             binaries=[],
             datas=[
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\config\\*.*', 'config'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\connect\\*.*', 'connect'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\document\\*.*', 'document'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\document\\pic\\*.*', 'document\\pic'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\model\\*.*', 'model'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\UI\\*.*', 'UI'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\UI\\icon\\*.*', 'UI\\icon'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\util\\*.*', 'util'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\widget\\*.*', 'widget'),
                 ('D:\\FFM\\code\\ffm_renderFarm_server\\baseConfig.ini', '.'),
             ],
             hiddenimports=[],
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
          name='FFM_RFM_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='D:\\FFM\\code\\ffm_renderFarm_server\\UI\\ffm_main.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='start')

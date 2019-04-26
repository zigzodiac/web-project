# -*- mode: python -*-

block_cipher = None


a = Analysis(['start.py'],
             pathex=['F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client'],
             binaries=[],
             datas=[('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\config.cfg', '.'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\config\\*.*', 'config'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\connect\\*.*', 'connect'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\path\\*.*', 'path'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\util\\*.*', 'util'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\widget\\*.*', 'widget'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\resource\\css\\*.*', 'resource\\css'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\resource\\images\\*.*', 'resource\\images'),
                    ('F:\\FFM\\Git\\FFM_renderFarm_client\\ffm_renderFarm_client\\resource\\ui\\*.*', 'resource\\ui'),
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
          name='FFM_RenderFarm_Client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='resource\\images\\ffm_main.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='FFM_RenderFarm_Client')
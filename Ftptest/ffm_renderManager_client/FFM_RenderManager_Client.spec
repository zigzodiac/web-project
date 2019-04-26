# -*- mode: python -*-

block_cipher = None


a = Analysis(['start.py'],
             pathex=['D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client'],
             binaries=[],
             datas=[('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\renderManagerConfig.ini', '.'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\config\\*.*', 'config'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\connect\\*.*', 'connect'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\document\\*.*', 'document'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\document\\pic\\*.*', 'document\\pic'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\model\\*.*', 'model'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\util\\*.*', 'util'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\widget\\*.*', 'widget'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\resource\\css\\*.*', 'resource\\css'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\resource\\images\\*.*', 'resource\\images'),
                    ('D:\\FFM\\T\\FFM-Pipeline\\code\\ffm_renderManager_client\\resource\\ui\\*.*', 'resource\\ui'),
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='FFM_RenderManager_Client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='resource\\images\\ffm_main.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='FFM_RenderManager_Client')
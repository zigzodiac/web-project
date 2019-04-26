# -*- mode: python -*-

block_cipher = None


a = Analysis(['start.py'],
             pathex=['D:\\FFM\\code\\ffm_renderManager_server'],
             binaries=[],
             datas=[
                 ("D:\\FFM\\code\\ffm_renderManager_server\\start.py", "."),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\config.ini", "."),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\checkMongo\\*.*", "checkMongo"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\config\\*.py", "config"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\connect\\*.py", "connect"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\database\\*.py", "database"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\model\\*.py", "model"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\util\\*.py", "util"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\util\\*.dll", "util"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\widget\\*.py", "widget"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\Resource\\css\\*.css", "Resource\\css"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\Resource\\doc\\*.*", "Resource\\doc"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\Resource\\icon\\*.*", "Resource\\icon"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\Resource\\pic\\*.*", "Resource\\pic"),
                 ("D:\\FFM\\code\\ffm_renderManager_server\\Resource\\ui\\*.ui", "Resource\\ui"),
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
          name='FFM_Render_Server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='D:\\FFM\\code\\ffm_renderManager_server\\Resource\\icon\\ffm_main.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='start')

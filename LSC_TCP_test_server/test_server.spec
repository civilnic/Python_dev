# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\SVN_SOGETI\\CAPITALISATION\\OCASIME\\Project_Tools\\PYTHON_TOOLS\\Python_dev\\LSC_TCP_test_server\\test_server.py'],
             pathex=['D:\\SVN_SOGETI\\CAPITALISATION\\OCASIME\\Project_Tools\\PYTHON_TOOLS\\Python_dev\\LSC_TCP_test_server'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='LSC_TCP_test_server',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='D:\\SVN_SOGETI\\CAPITALISATION\\OCASIME\\Project_Tools\\PYTHON_TOOLS\\Python_dev\\Compilation\\Python.ico')

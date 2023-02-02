from py2exe import freeze

freeze(
    options = {'py2exe': {'bundle_files': 3, 'compressed': True, 'dist_dir': 'SM64BruteforceGUIv1.0.2'},
               'includes': ['wx', 'wx.lib.filebrowsebutton', 'actions', 'common', 'config', 'gui', 'script_options', 'user_defined_script', 'numpy', 'queue', 'dataclasses', 'random'],
               'excludes': ['defaultmp']},
    windows = [{'script': 'gui.py',
                'icon_resources': [(0, 'img\\DorrieChamp.ico'), (1, 'img\\DorrieChamp.ico')],
                'dest_base': 'SM64BruteforceGUI'}],
    zipfile = 'library.zip',
    version_info = {'version': '1.0.2'}
)
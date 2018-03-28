import os
import tempfile
import clr


def base_assembly_path():
    try:
        return _getdevconfig()['BaseBinariesPath']
    except (IOError, KeyError):
        pass
    try:
        return _get_installed_path()
    except IOError:
        return ''


def _get_installed_path():
    import winreg
    latest_dir = ''

    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Wow6432Node\\National Instruments\\VeriStand\\') as vskey:
        r = winreg.QueryInfoKey(vskey)
        ver = 0
        for k in range(r[0]):
            with winreg.OpenKey(vskey, winreg.EnumKey(vskey, k)) as this_key:
                this_ver = int(winreg.QueryValueEx(this_key, 'VersionString')[0])
                if this_ver > ver:
                    latest_dir = winreg.QueryValueEx(this_key, 'InstallDir')[0]
                    ver = this_ver
    return os.path.join(latest_dir, 'nivs.lib', 'Reference Assemblies')


def _getdevconfig():
    import yaml
    cfgfile = os.environ["vsdev.yaml"]
    cfgfile = cfgfile.strip('"')
    with open(os.path.normpath(cfgfile), "r") as f:
        cfg = yaml.load(f.read())
    return cfg


clr.AddReference("System")
clr.AddReference("System.IO")
from System.IO import FileNotFoundException  # noqa: E402, I202 .net imports can't be at top of file.
try:
    # Try loading from the GAC first, dev/install folders second.
    clr.AddReference("NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi")
    clr.AddReference("NationalInstruments.VeriStand.RealTimeSequenceDefinitionApiUtilities")
    clr.AddReference("NationalInstruments.VeriStand.DataTypes")
    clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
except FileNotFoundException:
    clr.AddReference(os.path.join(base_assembly_path(),
                                  "NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi.dll"))
    clr.AddReference(os.path.join(base_assembly_path(),
                                  "NationalInstruments.VeriStand.RealTimeSequenceDefinitionApiUtilities.dll"))
    clr.AddReference(os.path.join(base_assembly_path(),
                                  "NationalInstruments.VeriStand.DataTypes.dll"))
    clr.AddReference(os.path.join(base_assembly_path(),
                                  "NationalInstruments.VeriStand.ClientAPI.dll"))


def dummy():
    """
    Do nothing because you're just a dummy.

    This dummy can be used by any module that imports internal to get rid of PEP8 errors about
    an import not being used. This internal module takes care of loading C# references, so most
    times it will only be imported but not actually used.
    """
    pass


# set the temporary folder to C:\Users\$USER\AppData\Local\Temp\python_rt_sequences
tempfile.tempdir = os.path.join(tempfile.gettempdir(), 'python_rt_sequences')
if not os.path.exists(tempfile.tempdir):
    os.makedirs(tempfile.tempdir)

import _winreg as winreg

hive_key_mapping = {"HKLM": winreg.HKEY_LOCAL_MACHINE, "HKCU": winreg.HKEY_CURRENT_USER, "HKU": winreg.HKEY_USERS}


def read_sub_keys(hive_key, reg_path):
    if not path_exists(hive_key, reg_path):
        return None
        # Get the value of a pre-mapped hive key, if that's what we were provided
    if hive_key in hive_key_mapping.keys():
        reg = winreg.OpenKey(hive_key_mapping[hive_key], reg_path)
    else:
        reg = winreg.OpenKey(hive_key, reg_path)

    sub_keys = []
    num_subkeys = winreg.QueryInfoKey(reg)[0]
    for i in range(0, num_subkeys):
        sub_keys.append(winreg.EnumKey(reg, i))
    winreg.CloseKey(reg)
    if not num_subkeys == 0:
        return sub_keys
    elif num_subkeys == 0:
        return None
    else:
        return None


def read_values(hive_key, reg_path):
    if not path_exists(hive_key, reg_path):
        return None
        # Get the value of a pre-mapped hive key, if that's what we were provided
    if hive_key in hive_key_mapping.keys():
        reg = winreg.OpenKey(hive_key_mapping[hive_key], reg_path)
    else:
        reg = winreg.OpenKey(hive_key, reg_path)

    values = {}
    num_values = winreg.QueryInfoKey(reg)[1]
    for i in range(0, num_values):
        values[winreg.EnumValue(reg, i)[0]] = winreg.EnumValue(reg, i)[1]
    winreg.CloseKey(reg)
    if not num_values == 0:
        return values
    else:
        return None


def path_exists(hive_key, reg_path):
    try:
        # Get the value of a pre-mapped hive key, if that's what we were provided.
        # Otherwise supply the hive_key value to OpenKey() directly
        if hive_key in hive_key_mapping.keys():
            reg = winreg.OpenKey(hive_key_mapping[hive_key], reg_path)
        else:
            reg = winreg.OpenKey(hive_key, reg_path)
    except WindowsError:
        return False
    winreg.CloseKey(reg)
    return True

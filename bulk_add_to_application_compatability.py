from __future__ import print_function
import _winreg as winreg
import os
import re
import time
import fnmatch
import sys
#import argparse

_name = "Bulk Windows Application Compatibility Settings Utility"
_version = "1.0.0"
_description = "Utility that searches for executable files matching a file mask in a given directory and adds them " \
               "to the Windows application compatibility settings registry key"

#parser = argparse.ArgumentParser(prog=_name, version=_version)
#parser.add_argument()

#########
# Begin configuration options
#########

# Quiet mode prevents writing to stdout, however error messages will still be written to stderr
quiet = False

# File masks to search for and add to the registry with application compatibility settings
include_extensions = ['*.exe', '*.com']

# base directory to recursively search for files matching the above file masks
# If this is None, the current working directory will be used instead, but the variable MUST be set
# working_dir = r'C:\some\dir\change\me'
working_dir = None

# Hostname to connect remote registry to. If local registry is to be used, this value should be set to None
# Remote registry connection capability is provided by the _winreg API and supported by the script but is
#   completely UNTESTED in the context of this tool.
registry_host = None
#registry_host = someserver.somedomain.tld

# Registry hive to connect to as a _winreg hive object. By default it is winreg.HKEY_CURRENT_USER and probably
#   shouldn't be changed.
# This MUST be a winreg hive object. Simply using the hive name as a string WILL NOT WORK!
# Using winreg.HKEY_LOCAL_MACHINE does not work under Windows 8 (With UAC on or off) and no other platforms
#   have been tested, YMMV
registry_hive = winreg.HKEY_CURRENT_USER

# Registry key within the selected hive that stores the application compatibility settings. Do not modify unless
# you understand what you're doing. 99.9% of users will not need to modify this EVER.
registry_key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers'

# Registry value data to set for all new and updated values
# Registry format is something like: HIVE\KEY\KEY\KEY\KEY VALUE_NAME:VALUE_TYPE:VALUE_DATA
compat_properties = r'~ RUNASADMIN WIN7RTM'

# Continue adding new registry entries or updating existing ones if there is an error writing the previous entry
resume_on_error = True

# Perform a backup of the registry hive+key before making any modifications.
# Currently DOES NOT WORK!
do_registry_backup = False

# Filename to store the registry backup. Defaults to the user's home directory in an aptly named & timestamped file
backup_filename = os.path.join(os.path.expanduser("~"),
                               'AppCompat_Registry_Backup-'
                               + time.strftime("%a_%d_%b_%Y_%H-%M-%S")
                               + '.reg')
continue_if_backup_fails = True

#########
# End of configuration options
#########

def print_message(message):
    if not quiet:
        print("[*] " + str(message))


def print_error(message, stderr=True):
    if stderr:
        print("[!] " + message, file=sys.stderr)
    else:
        print("[!] " + message)

# List to store files matching the include_extensions file masks
executable_files = []
existing_registry_values = {}
files_to_update = []
files_to_add = []
registry_backup_completed = (False, None)
values_added = 0
values_updated = 0
values_modified_total = 0
values_skipped = 0

if not working_dir:
    working_dir = os.getcwd()

# Translate our list of file extension masks to regular expressions for use with re.match()
include_extensions_regex = r'|'.join([fnmatch.translate(x) for x in include_extensions])

# Find files recursively in the working_dir that match the specified file masks
print_message("Recursing directory: " + working_dir + " for files matching: " + ','.join(include_extensions))
for root, dirs, files in os.walk(working_dir):
    executable_files += [f for f in [os.path.join(root, f) for f in files] if re.match(include_extensions_regex, f)]

# Quit with informative information if no matching files are found
if executable_files is None or len(executable_files) < 0:
    print_error("No files matching provided file mask(s) in the directory provided. Unable to continue.")
    print_error("Search directory: " + working_dir)
    print_error("File mask(s): " + ','.join(include_extensions))
    sys.exit(1)

# Open the specified registry hive (Remote or local. If local, registry_host should be None
if registry_host is None:
    print_message("Connecting to local Windows registry.")
else:
    print_message("Connecting to Windows registry on host: " + registry_host)

with winreg.ConnectRegistry(registry_host, registry_hive) as open_registry_hive:
    # Open the registry key
    with winreg.OpenKey(open_registry_hive, registry_key, 0, winreg.KEY_ALL_ACCESS) as open_registry_key:

        if do_registry_backup:
            if registry_backup_completed == (True, registry_key):
                print_error("Registry backup for key \"" + registry_key + "\" has already been completed")

            print_message("Backing up registry key to file: " + backup_filename)
            try:
                winreg.SaveKey(open_registry_key, backup_filename)
            except WindowsError as ex:
                print_error("Exception caught while saving registry key backup.")
                print_error("Key: " + registry_key)
                print_error("Filename: " + backup_filename)
                print_error("Exception message: " + str(ex.message))
                print_error("Exception filename: " + str(ex.filename))
                print_error("Windows error: " + str(ex.winerror))

                if not continue_if_backup_fails:
                    print_error("Quitting due to failure to back up the registry key before modifying values.")
                    raise
            else:
                registry_backup_completed = (True, registry_key)
                print_message("Registry key successfully saved to file")

        # Retrieve the existing values within the opened key and store them in existing_registry_values dict
        for i in range(0, winreg.QueryInfoKey(open_registry_key)[1]):
            value_pair = winreg.EnumValue(open_registry_key, i)
            existing_registry_values[value_pair[0]] = value_pair[1]

        # Check if any of the executables in executable_files already exists in a value, if so put them in a list of
        # tuples,
        # if not, also put them in a list
        # List of tuples [(property,value)]
        files_to_update = [(f, v) for f, v in existing_registry_values.iteritems() if f in executable_files]
        # List of tuples [(property,value)]
        files_to_add = [(f, compat_properties) for f in executable_files if f not in existing_registry_values.keys()]

        # Insert new values & data from files_to_add
        for (f, v) in files_to_add:
            try:
                #winreg.SetValue(open_registry_key,f,1,v)
                winreg.SetValueEx(open_registry_key, f, winreg.REG_SZ, winreg.REG_SZ, v)
            except WindowsError as ex:
                print_error("Exception caught while creating new registry subkey.")
                print_error("Key: " + registry_key)
                print_error("Name: " + f)
                print_error("Value: " + v)
                print_error("Exception message: " + str(ex.message))
                print_error("Exception filename: " + str(ex.filename))
                print_error("Windows error: " + str(ex.winerror))

                if not resume_on_error is True:
                    raise ex
            else:
                values_added += 1
                values_modified_total += 1
                print_message("New value created for file: " + f)
                # Update existing values with new/updated (Or possibly the same) data
        for (f, v) in files_to_update:
            # Overwrite/update the original value data with our static value in compat_properties if they differ,
            # else, don't process the value as no update is needed
            if not v == compat_properties:
                v = compat_properties
            else:
                # No update to the key is needed as new & existing values are identical
                values_skipped += 1
                print_message("Skipped updating value as existing and new values are identical: " + f)
                continue

            try:
                winreg.SetValueEx(open_registry_key, f, winreg.REG_SZ, winreg.REG_SZ, v)
                #winreg.SetValue(open_registry_key,f,1,v)
            except WindowsError as ex:
                print_error("Exception caught while updating existing registry subkey.")
                print_error("Key: " + registry_key)
                print_error("Name: " + f)
                print_error("Value: " + v)
                print_error("Exception message: " + ex.message)
                print_error("Exception filename: " + ex.filename)
                print_error("Windows error: " + ex.winerror)

                if not resume_on_error is True:
                    raise ex
            else:
                values_updated += 1
                values_modified_total += 1
                print_message("Updated existing key for file: " + f)

print_message("Registry values added: " + str(values_added))
print_message("Registry values modified: " + str(values_updated))
print_message("Registry value modifications skipped (Pre-existing): " + str(values_skipped))
print_message("Total registry modifications performed: " + str(values_modified_total))

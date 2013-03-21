Batch Windows Compatibility Settings Tool
================================
Written by Robert McGinley - 3/2013
License: Apache-2.0

Searches for executable files recursively in a given path or the current working directory,  which are then added to the Windows Application Compatibility Settings with "Run as Administrator" and "Windows 7" mode properties.

Developed under Windows 8 with Python 2.7.2 32bit
Uses pywin32._winreg to manipulate the Windows registry hive of HKEY_CURRENT_USER. I was unable to get this code working for the HKEY_LOCAL_MACHINE hive, so that the compatability settings are 'global' to the system. I suspect it's an access rights/permission/authority windows thing that I don't totally understand.
As it sits, it will add all of the .exe and .com files recursively found from working_dir.

working_dir

Configuration Parameters
--------------------------------
* working_dir
    * String that specifies the root path to begin the file search. If this path does not exist or the object = None (e.g. is NoneType), the search will start from whatever directory the script was started from (a.k.a. %CD% or $PWD under Posix) as Python sees it from os.getcwd()
    * No matter what, this object must exist or the script will throw an exception and fail miserably

* quiet
    * Suppresses informational output to stdout. Error messages and the like will still be output to stderr

* include_extensions
    * List of file mask extensions to treat as an 'executable'. Files found with these extensions will be operated upon

* registry_host
    * Hostname or ip address of the Windows registry to connect to and manipulate. None (NoneType) is the default and denotes the local machine. Probably best not to change this unless you know exactly what you're doing (Manipulating a remote registry hive based on local absolute paths to executable files... Hmm...)

* registry_hive
    * The registry hive to connect to and manipulate

* registry_key
    * The registry key where the Application Compatability settings live

* compat_properties
    * The value data used to identify what specific compatability settings are applied to all the executables.
    * By default the value is ```~ RUNASADMIN WIN7RTM``` which specifies "Run as administrator" and "Windows 7" mode.
        * The default will only work under Windows 8 as I don't think Windows 7 has a way to emulate Windows 7...

* resume_on_error
    * Continues if an error occurs

* do_registry_backup
    * Tries to back up the registry key before modification takes place

* backup_filename
    * Filename to write the backup to

* continue_if_backup_fails
    * Proceed with modifications even if the backup fails

Changelog
--------------------------------
* v1.0 - 3/20/2013 - Initial release

Todo
--------------------------------
* Integrate argparse to take command line arguments instead of the static objects/variables defined in the beginning of the script
* Provide list of possible alternative compatibility settings - See: http://msdn.microsoft.com/en-us/library/bb757005.aspx
* 

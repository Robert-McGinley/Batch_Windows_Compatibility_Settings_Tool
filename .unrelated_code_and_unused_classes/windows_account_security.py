import win32security
import win32file
import win32api
import ntsecuritycon
import win32con
import os


class windows_security(object):
    def __init__(self):
        """
        do stuff

        """
        self.sids = {
            'current_user': win32security.GetTokenInformation(self.token_handle, ntsecuritycon.TokenUser)[0],
            'power_user': win32security.LookupAccountName('', 'Power Users')[0],
            'administrators': win32security.LookupAccountName('', 'Administrators')[0],
            'everyone': win32security.LookupAccountName('', 'Everyone')[0],
            'users': win32security.LookupAccountName('', 'Users')[0]
        }

        self.acl = win32security.ACL()

        self.account_authority_privs = (
            (win32security.LookupPrivilegeValue('', ntsecuritycon.SE_SECURITY_NAME), win32con.SE_PRIVILEGE_ENABLED),
            (win32security.LookupPrivilegeValue('', ntsecuritycon.SE_RESTORE_NAME), win32con.SE_PRIVILEGE_ENABLED),
        )
        self.process_handle = win32api.GetCurrentProcess()
        self.token_handle = win32security.OpenProcessToken(self.process_handle,
                                                           win32security.TOKEN_ALL_ACCESS | win32con.TOKEN_ADJUST_PRIVILEGES)

        self.sids['current_user'] = win32security.GetTokenInformation(self.token_handle, ntsecuritycon.TokenUser)[0]
        self.sids['power_user'] = win32security.LookupAccountName('', 'Power Users')[0]
        self.sids['administrators'] = win32security.LookupAccountName('', 'Administrators')[0]
        # Todo: Is the group reference for 'everyone', Everyone or EveryOne? Will the lookup work correctly regardless? e.g. case insensitive?
        self.sids['everyone'] = win32security.LookupAccountName('', 'Everyone')[0]
        self.windows_temp_path = win32api.GetTempPath()


    def check_user_account_priv(self, account):
        """


        :rtype : win32security
        :param account: str
        """
        pass

    def _elevate_process_token_privileges(self, tokenhandle, sid):
        modified_privileges = win32security.AdjustTokenPrivileges(tokenhandle, 0, self.account_authority_privs)

    def set_privs(self, target, privileges):
        """

        :rtype : bool
        """
        authority = self.account_authority_privs


winsec = windows_security()
winsec.set_privs()



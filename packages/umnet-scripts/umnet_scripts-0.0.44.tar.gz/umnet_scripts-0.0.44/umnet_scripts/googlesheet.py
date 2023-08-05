#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .cyberark import Cyberark


class UMGoogleSheet(object):
    def __init__(self):
        cyberark = Cyberark("UMNET")
        self.scope_app = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.service_account_email = str(cyberark.query_cyberark("gsheet_api_service_account_email"))
        self.project_id = str(cyberark.query_cyberark("gsheet_api_project_id"))
        self.client_id = str(cyberark.query_cyberark("gsheet_api_client_id"))
        self.private_key_id = str(cyberark.query_cyberark("gsheet_api_key_id"))
        self.private_key = str(cyberark.query_cyberark("gsheet_api_private_key")).replace("\\n", "\n")

    def _gsheet_auth(self):
        json_creds = {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.service_account_email,
            "client_id": self.client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/" + self.service_account_email.replace("@", "%40"),
        }
        cred = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, self.scope_app)

        # authorize the clientsheet
        return gspread.authorize(cred)


    def open_spreadsheet(self, url_or_key):
        '''
        Opens a spreadsheet by url or by key. Detects a url by looking for 'https'
        '''
        self._client = self._gsheet_auth()
        if url_or_key.startswith('http'):
            self._ss = self._client.open_by_url(url_or_key)
        else:
            self._ss = self._client.open_by_key(url_or_key)

    def get_worksheet(self, ws_name, return_as_dict=True):
        '''
        Gets a worksheet by name. If return as dict is set to true (default is yet),
        will return the results of "get all records". Otherwise will return a worksheet object.
        '''
        if "_ss" not in self.__dict__:
            raise ValueError(f'Sheet has not been opened, use "open_sheet(url_or_key)" to open the sheet first!')

        ws = self._ss.worksheet(ws_name)
        if return_as_dict:
            return ws.get_all_records()
        else:
            return ws

    def open_and_get_worksheet(self, url_or_key, ws_name, return_as_dict=True):
        """
        Opens a spreadsheet and gets a worksheet by name from that spreadsheet.
        """
        self.open_spreadsheet(url_or_key)
        return self.get_worksheet(ws_name, return_as_dict=True)
import pickle
import os

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import debug

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class TiltHyrdrometer:

  def __init__(self, config):
    self._sheet_id = config.fermentation_stats_google_sheets_id
    self.current_specific_gravity = None
    self.first_specific_gravity = None
    self.fermentation_rate_per_day = None
    self.days = None
    self.high_specific_gravity = None
    self.low_specific_gravity = None

    self.current_temp = None
    self.avg_temp = None
    self.high_temp = None
    self.low_temp = None

    self.apparent_attenuation = None
    self.standard_method_abv = None
    self.days_at_current_specific_gravity = None
    self.expected_final_gravity = None
    self.percent_completed = None

  def fetch(self):
    debug.log("Fetching Tilt Hydrometer data from google sheets")

    sheet = self._get_sheets().values().get(spreadsheetId=self._sheet_id,
                                            range="Report",
                                            majorDimension='COLUMNS'
                                            ).execute()

    values = sheet['values']
    val_col = values[1] # Column B

    self.current_specific_gravity = val_col[7]
    self.first_specific_gravity = val_col[8]
    self.fermentation_rate_per_day = val_col[9]
    self.days = val_col[10]
    self.high_specific_gravity = val_col[11]
    self.low_specific_gravity = val_col[12]

    self.current_temp = val_col[14]
    self.avg_temp = val_col[15]
    self.high_temp = val_col[17]
    self.low_temp = val_col[18]

    self.apparent_attenuation = val_col[20]
    self.standard_method_abv = val_col[21]
    self.days_at_current_specific_gravity = val_col[22]
    self.expected_final_gravity = val_col[23]
    self.percent_completed = val_col[24]

  def _get_sheets(self):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
          'credentials.json', SCOPES)
        creds = flow.run_console(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet

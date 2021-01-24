# Google Sheets API Initial Setup
To setup Google Sheets integration, follow these steps.  They are roughly based off of https://developers.google.com/sheets/api/quickstart/python

### Set up the credentials.json file

Put the supplied `credentials.json` file in your `mlb-led-scoreboard` directory.

### Install the google client libraries

In the `mlb-led-scoredboard` directory, run

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Run the scoreboard once to save Google Sheets token

Something like:

```
python -u main.py --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=4 --led-cols=64
```

The program will pause with the message `Please visit this URL to authorize this application:`

Go to that URL and follow the steps to authorize the program to view google sheets files.
This will include clicking past a page that says "Google hasn't verified this app".
At the end, an authorization code will be provided - copy that back into the console after
`Enter the authorization code:` and press enter.

This will create a file `token.pickle` that the scoreboard will use on future runs to authenticate.
Don't let anyone get a hold of both `token.pickle` and `credentials.json`, otherwise they will be able to
read all of your google sheets.

### Configure the Google Sheet ID in `config.json`

Change `google_sheets_id` in `config.json` based on the URL of the target sheet.

A URL of the form...

```
https://docs.google.com/spreadsheets/d/afjlsdklkj
```

...has the ID `afjlsdklkj`.
## instructions
* create env
```bash
python -m venv myenv
```
* Activate Env
```cmd
myenv\Scripts\activate
```

Mac/Linux
```bash
source venv/bin/activate
```
* To deactivate env
```bash
deactivate
```
* Install Dependencies
```bash 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib ollama flask gspread waitress python-dotenv
```
* Run Redis
```bash
sudo service redis-server start
```
* update requirements.txt
```bash
pipreqs /path/to/project
```
* Run code: 
```bash
python app.py
```

## About Credentials_oauth
* The very first time we should save a client json downloaded from Google cloud console.
* We should comment following lines:
  ```python
  if os.path.exists('credentials_oauth.json'):
    creds = Credentials.from_authorized_user_file('credentials_oauth.json', SCOPES)
  ```
* It would prompt on browser to login

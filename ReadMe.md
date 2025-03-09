## instructions
* Run Redis
```bash
sudo service redis-server start
```
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
pip install -r /path/to/requirements.txt
```
* Run Redis Server
```bash
redis-server
```
* Run RQ worker
```bash
rq worker
```
* update requirements.txt
```bash
pipreqs /path/to/project
```
* Run code: 
```bash
python run.py
```

## About Credentials_oauth
* The very first time we should save a client json downloaded from Google cloud console.
* We should comment following lines:
  ```python
  if os.path.exists('credentials_oauth.json'):
    creds = Credentials.from_authorized_user_file('credentials_oauth.json', SCOPES)
  ```
* It would prompt on browser to login

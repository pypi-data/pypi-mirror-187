# TestRail Interface


## Pypi
https://pypi.org/project/testrail-interface/
### Install
```bash
pip install testrail-interface
```
### Usage
```bash
python3 -m testrail_interface -h
```
### Build
Make sure you have the latest version of PyPA’s build installed:
```bash
python3 -m pip install --upgrade build
```
Now run this command from the same directory where pyproject.toml is located:
```bash
python3 -m build
```
### Upload to Pypi
```bash
python3 -m twine upload dist/*
```


## Docker
### Build
```bash
docker build -t nexus.start-i.ru:8083/testrail_interface --rm .
```
### Nexus container registry
```bash
# Login
docker login nexus.start-i.ru:8083 --username $USERNAME --password $PASSWORD
# Push
docker push nexus.start-i.ru:8083/testrail_interface
```

### Usage
```bash
# Start
docker run -dit --name testrail_reporter --rm \
        -e TR_DOMAIN \
        -e TR_USERNAME \
        -e TR_API_KEY \
        -e TR_PROJECT_ID \
        --mount type=bind,source="$(pwd)"/$TESTS_DIR,target=/home/app_user/$TESTS_DIR \
        nexus.start-i.ru:8083/testrail_interface
# Open help
docker exec -it testrail_reporter python testrail_interface.py -h
# Send report
docker exec -it testrail_reporter python testrail_interface.py send_report -f $TESTS_DIR/report_.json
# Stop
docker stop testrail_reporter
```

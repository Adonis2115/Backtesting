from fyers_api import fyersModel
from fyers_api import accessToken
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from chromedriver_py import binary_path
import time
import json

def getToken():
    f = open('./brokers/fyers/credentials.json')
    credentials = json.load(f)
    appID = credentials['appID']
    secretID = credentials['secretID']
    url = credentials['url']
    fyers_ID = credentials['fyers_ID']
    fyers_password = credentials['fyers_password']
    pan = credentials['pan']
    session=accessToken.SessionModel(client_id=appID,
            secret_key=secretID,redirect_uri=url, 
            response_type='code', grant_type='authorization_code',
            state='state')

    authUrl = session.generate_authcode()
    driver =  webdriver.Chrome(executable_path=binary_path)
    with driver:
        driver.get(authUrl)
        if driver.current_url == authUrl:
            login_id = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath('//*[@id="fyers_id"]'))
            login_id.send_keys(fyers_ID)
            password = driver.find_element_by_xpath('//*[@id="password"]')
            password.send_keys(fyers_password)
            panform = driver.find_element_by_xpath('//*[@id="pancard"]')
            panform.send_keys(pan)
            notWeb = driver.find_element_by_xpath('//*[@id="myForm"]/div[6]/p/label/span')
            notWeb.click()
            login = driver.find_element_by_xpath('//*[@id="btn_id"]')
            login.click()
        while authUrl == driver.current_url:
            print('Getting Auth Code......')
        newUrl = driver.current_url
        authStart = newUrl.find('auth_code=') + 10
        authEnd = newUrl.find('&state=')
        auth_code = newUrl[authStart:authEnd]
        
        credentials['auth_code'] = auth_code

        f = open("./brokers/fyers/credentials.json", "w")
        json.dump(credentials, f)
        f.close()

    f = open('./brokers/fyers/credentials.json')
    credentials = json.load(f)

    auth_code = credentials['auth_code']

    session.set_token(auth_code)
    response = session.generate_token()

    token = response["access_token"]
    credentials['token'] = token

    f = open("./brokers/fyers/credentials.json", "w")
    json.dump(credentials, f)
    f.close()

    f = open('./brokers/fyers/credentials.json')
    credentials = json.load(f)

f = open('./brokers/fyers/credentials.json')
credentials = json.load(f)
appID = credentials['appID']
token = credentials['token']

fyers = fyersModel.FyersModel(client_id=appID, token=token, log_path="C:/Users/Himanshu Pandey/Documents/Project/Code/backtrader/brokers/fyers/logs")
is_async = True

if fyers.get_profile()['code'] != 200:
    getToken()
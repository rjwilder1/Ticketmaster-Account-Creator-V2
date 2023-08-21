import time
from playwright.sync_api import BrowserContext, sync_playwright
from undetected_playwright import stealth_sync
from bs4 import BeautifulSoup
import requests
import time
import random
from collections import OrderedDict
import configparser
from itertools import cycle

GlobalPassword = "L@rgeB0l@s69*"
locales = OrderedDict([
    ('en-US', 1)
])

Proxies = []
FinishedAccounts = []
BadPhoneNumbers = []
PhoneNumbers = []
config= configparser.ConfigParser()
config.read(r'config.ini')
URL = config['CONFIG']['smsurl'].split(", ")

def GetCode(PhoneNum):
    global URL
    FoundNumber = False
    while not FoundNumber:
        time.sleep(1)
        for SMSURL in URL:
            response = requests.get(SMSURL)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find('table')
            if table:
                msgs = table.find_all('tr')
                if len(msgs) >= 1:
                    td_elements = msgs[0].find_all('td')
                    if len(td_elements) >= 3:
                        PhoneNumber = td_elements[0].get_text()
                        if PhoneNum in PhoneNumber:
                            Code1 = td_elements[2].get_text() 
                            c = Code1.split()
                            Code = c[0]
                            FoundNumber = True
                            return Code
            if FoundNumber:
                break

def rwait():
    time.sleep(random.uniform(1, 3))
    
#Fill Functions
def FillPN():
    global PhoneNumbers
    with open('PhoneNumbers.txt', "r") as file:
        for line in file:
            PhoneNumbers.append(line[:10])

def FillBadPN():
    global BadPhoneNumbers
    with open('BadTMPhoneNumbers.txt', "r") as file:
        for line in file:
            BadPhoneNumbers.append(line[:10])

def FillFinishedAccounts():
    global FinishedAccounts
    with open('GeneratedTMAccounts.txt', "r") as file:
        for line in file:
            ac = line.split(',')
            FinishedAccounts.append(ac[0])

def FillProxies():
    global Proxies
    with open('proxies.txt', "r") as file:
        for line in file:
            Proxies.append(line)

#Call Fill Functions
FillProxies()
FillPN()
FillBadPN()
FillFinishedAccounts()

#Cycles
CycleProxies = cycle(Proxies)
CyclePN = cycle(PhoneNumbers)

def run(context: BrowserContext, line):
    global PhoneNumbers
    global BadPhoneNumbers
    global CyclePN
    global GlobalPassword
    global GoodEmail
    page = context.new_page()
    fullline = line.split(',')
    ThisEmail = fullline[0]
    ThisPhoneNumber = fullline[1]
    GoodNumber = False
    GoodEmail = False
    FakeFirst = fake.name().split()[0]
    FakeLast = fake.name().split()[1]
    FakeZip = fake.postcode()
    page.goto("http://ticketmaster.com/")
    rwait()
    if page.query_selector("text=Proxy Error:"):
        print("Error with proxy")
        return
    if page.query_selector("text=Pardon the Interruption"):
        print("Proxy is unusable")
        return True
    page.locator("xpath=//span[text()='Sign In']").click()
    rwait()
    if page.query_selector("text=Pardon the Interruption"):
        print("Proxy is unusable")
        return True
    page.locator("xpath=//button[text()='Sign Up']").click()
    rwait()
    if page.query_selector("text=Pardon the Interruption"):
        print("Proxy is unusable")
        return True
    page.locator("xpath=//input[@type='email']").fill(ThisEmail)
    rwait()
    page.locator("xpath=//input[@name='password']").fill(GlobalPassword)
    rwait()
    page.locator("xpath=//input[@name='firstName']").fill(FakeFirst)
    rwait()
    page.locator("xpath=//input[@name='lastName']").fill(FakeLast)
    rwait()
    page.locator("xpath=//input[@name='postalCode']").fill(FakeZip)
    rwait()
    page.locator("xpath=//span[text()='Next']").click()
    rwait()
    while GoodEmail == False:
        if page.query_selector("text=It Looks Like You Already Have an Account") is None:
            GoodEmail = True
            break
        else:
            print("Email already exists as a ticketmaster account: " + ThisEmail)
            with open("GeneratedTMAccounts.txt", "a") as file:
                file.write(f"{ThisEmail},,{GlobalPassword},\n")
            return
    page.locator("xpath=//input[@name='phoneNumber']").fill(ThisPhoneNumber)
    rwait()
    page.locator("xpath=//span[text()='Next']").click()
    rwait()

    while GoodNumber == False:
        if page.query_selector("text=phone number you entered is not supported") is None:
            GoodNumber = True
            break
        else:
            with open('BadTMPhoneNumbers.txt', "a") as file:
                file.write(ThisPhoneNumber + "\n")
            BadPhoneNumbers.append(ThisPhoneNumber)
            ThisPhoneNumber = next(CyclePN)
            if ThisPhoneNumber not in BadPhoneNumbers:
                page.locator("xpath=//input[@name='phoneNumber']").fill(ThisPhoneNumber)
                rwait()
                page.locator("xpath=//span[text()='Next']").click()
                rwait()
        time.sleep(1)

    Code = GetCode(ThisPhoneNumber[:10])
    page.locator("xpath=//input[@name='otp']").fill(Code)
    page.keyboard.press("Enter")
    rwait()
    page.locator("text=My Account")
    with open('GeneratedTMAccounts.txt', 'a') as y:
        y.write(f"{ThisEmail},{ThisPhoneNumber},{GlobalPassword},{FakeZip}\n")
    print("Ticketmaster account generated for: " + ThisEmail)

def bytedance():
    global CycleProxies
    global FinishedAccounts
    with open("GmailAccounts.txt", "r") as file:
        for line in file:
            splitter = line.split(',')
            if splitter[0] not in FinishedAccounts:
                with sync_playwright() as p:
                    Proxy = next(CycleProxies)
                    browser = p.chromium.launch(headless=False, #proxy={"server":f"{Proxy}"}
                    proxy={"server": "http://131.153.163.178:7383", "username": "LV10724126-nZf14an7XY-79", "password": "o1S2YYnF5v4ZlyQHpEQx"}
                )
                    context = browser.new_context()
                    stealth_sync(context)
                    whatwentwrong = run(context, line)
                    while whatwentwrong == True:
                        whatwentwrong = run(context, line)
                        print("Failed. Relaunching")
                        time.sleep(5)
                    context.close()
                    browser.close()
    input("Finished creating accounts")

bytedance()
# LinkedinMama.py
#
# Original Scraper - @DisK0nn3ct (https://github.com/DisK0nn3cT/linkedin-gatherer)
# Updated Scraper - @vysecurity (https://github.com/vysecurity/LinkedInt/blob/master/LinkedInt.py)
# 
# Modified Script - @bigb0ss
# 
# Updates:
#   1) Simplified and cleaned up some script outputs. 
#   2) Added random delays (0-3) between scraping pages
#   3) Modified only output file to .csv
#   4) Auto companyID search seemed to be unrealiable for some companies that have multiple IDs --> Modified to provide exact companyID from Linkedin

#!/usr/bin/python

class color:
    yellow = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end  = '\033[0m'

import sys
import re
import time
import requests
import subprocess
import json
import argparse
import cookielib
import os
import urllib
import math
import urllib2
import string
import ConfigParser
from bs4 import BeautifulSoup
from thready import threaded
from random import randint
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')

""" Setup Argument Parameters """
parser = argparse.ArgumentParser(description='[*] Linkedin User Scraper')
parser.add_argument('-k', '--keywords', help='Keywords to search & create output to file')
parser.add_argument('-c', '--companyid', help='facetCurrentCompany= parameter value')
parser.add_argument('-e', '--email', help='Company email domain')
parser.add_argument('-n', '--naming', help='User naming scheme: \n                  [0] Auto (hunter.io) \n    [1] FirstLast \n    [2] FirstMiddleLast \n    [3] FLast \n    [4] FirstL \n    [5] First.Last \n    [6] Last.First \n')
args = parser.parse_args()

""" Login Credentials """
config = ConfigParser.RawConfigParser()
config.read("LinkedinMama.cfg")
api_key = config.get('API_KEYS', 'hunter_api')
username = config.get('CREDS', 'linkedin_user')
password = config.get('CREDS', 'linkedin_pass')

def banner():
    print
    print("  _      _____ _   _ _  ________ _____ _____ _   _ __  __          __  __           ")         
    print(" | |    |_   _| \ | | |/ /  ____|  __ \_   _| \ | |  \/  |   /\   |  \/  |   /\     ")   
    print(" | |      | | |  \| | ' /| |__  | |  | || | |  \| | \  / |  /  \  | \  / |  /  \    ")   
    print(" | |      | | | . ` |  < |  __| | |  | || | | . ` | |\/| | / /\ \ | |\/| | / /\ \   ")  
    print(" | |____ _| |_| |\  | . \| |____| |__| || |_| |\  | |  | |/ ____ \| |  | |/ ____ \  ") 
    print(" |______|_____|_| \_|_|\_\______|_____/_____|_| \_|_|  |_/_/    \_\_|  |_/_/    \_\\")
    print("                                                                  [bigb0ss]         ")
    print                                                                               
    print(color.blue + "[*] Linkedin Intelligence" + color.end)
    print(color.blue + "[*] Original Scraper by @DisK0nn3ct" + color.end)
    print(color.blue + "[*] Updated Scraper by @vysecurity" + color.end)
    print(color.blue + "[*] This Scraper by @bigb0ss" + color.end)   
    print

### Linkedin Login
def login():
    url = 'https://www.linkedin.com'
    s = requests.Session()
    r = s.get(url + '/uas/login?trk=guest_homepage-basic_nav-header-signin')
    if r.status_code == 200:
        print '[+] Welcome to Linkedin!'
    else:
        print color.red + '[-] Linkedin hates you!' + color.end
        sys.exit(0)
    p = BeautifulSoup(r.content, "html.parser")
    
    csrf = p.find(attrs = {'name' : 'loginCsrfParam'})['value']
    csrf_token = p.find(attrs = {'name' : 'csrfToken'})['value']
    sid_str = p.find(attrs = {'name' : 'sIdString'})['value']
    #print csrf
    #print csrf_token
    #print sid_str

    postData = {'csrToken' : csrf_token,
                'loginCsrfParam' : csrf,
                'sIdString' : sid_str,
                'session_key' : username,
                'session_password' : password
                }

    r = s.post(url + '/checkpoint/lg/login-submit', data=postData)
    p = BeautifulSoup(r.content, "html.parser")
    try:
        cookie = requests.utils.dict_from_cookiejar(s.cookies)
        cookie = cookie['li_at']
    except:
        print color.red + "[-] Linkedin Credentials Invalid..." + color.end
        sys.exit(0)
    return cookie

### Linkedin Search
def get_search():
    csv = []

    if bCompany == False:
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List()&keywords=%s&origin=OTHER&q=guided&start=0" % search
    else:
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=0" % (companyID)
    
    headers = {'Csrf-Token':'ajax:0397788525211216808', 'X-RestLi-Protocol-Version':'2.0.0'}
    cookies['JSESSIONID'] = 'ajax:0397788525211216808'
    r = requests.get(url, cookies=cookies, headers=headers)
    content = json.loads(r.text)
    data_total = content['elements'][0]['total']

    ### 40 results per page
    pages = int(math.ceil(data_total /40.0))
    if pages == 0:
        pages == 1

    if data_total % 40 == 0:
        pages = pages - 1

    if pages == 0:
        print color.red + "[-] Use quotes in the search name" + color.end
        sys.exit(0)

    print "[+] %i Results Found" % data_total
    if data_total > 1000:
        pages = 25
        print "[*] Linkedin only allows 1000 results."
    print "[*] Fetching %i Pages" % pages
    
    for p in range(pages):
        # Results from each page
        if bCompany == False:
            url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List()&keywords=%s&origin=OTHER&q=guided&start=%i" % (search, p*40)
        else:
            url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=%i" % (companyID, p*40)
        r = requests.get(url, cookies = cookies, headers = headers)
        content = r.text.encode('UTF-8')
        content = json.loads(content)
        print "[+] Fetching page %i with %i results" % (p,len(content['elements'][0]['elements']))
        
        for c in content['elements'][0]['elements']:
            if 'com.linkedin.voyager.search.SearchProfile' in c['hitInfo'] and c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['headless'] == False:
                try:
                    data_industry = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['industry']
                except:
                    data_industry = ""
                data_firstname = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['firstName']
                data_firstname = data_firstname.lower()
                data_lastname = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['lastName']
                data_lastname = data_lastname.lower()
                data_slug = "https://www.linkedin.com/in/%s" % c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']
                data_occupation = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['occupation']
                data_location = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['location']

                # Massage for Weird LastNames
                parts = data_lastname.split()

                name = data_firstname + " " + data_lastname
                fname = ""
                mname = ""
                lname = ""

                if len(parts) == 1:
                    fname = data_firstname
                    mname = '?'
                    lname = parts[0]
                elif len(parts) == 2:
                    fname = data_firstname
                    mname = parts[0]
                    lname = parts[1]
                elif len(parts) >= 3:
                    fname = data_firstname
                    lname = parts[0]
                else:
                    fname = data_firstname
                    lname = '?'

                fname = re.sub('[^A-Za-z]+', '', fname)
                mname = re.sub('[^A-Za-z]+', '', mname)
                lname = re.sub('[^A-Za-z]+', '', lname)

                if len(fname) == 0 or len(lname) == 0:
                    continue

                # Username Scheme Generator
                # [0] Auto (hunter.io) 
                # [1] FirstLast
                if prefix == "1" or prefix == 'firstlast':
                    user = '{}{}'.format(fname, lname)
                # [2] FirstMiddleLast 
                if prefix == "2" or prefix == 'fistmlast':
                    if len(mname) == 0:
                        user = '{}{}{}'.format(fname, mname, lname)
                    else:
                        user = '{}{}{}'.format(fname, mname[0], lname)
                # [3] FLast 
                if prefix == "3" or prefix == 'flast':
                    user = '{}{}'.format(fname[0], lname)
                # [4] FirstL  
                if prefix == "4" or prefix == 'firstl':
                    user = '{}{}'.format(fname, lname[0])
                # [5] First.Last 
                if prefix == "5" or prefix == 'first.last':
                    user = '{}.{}'.format(fname, lname)
                # [6] Last.First
                if prefix == "6" or prefix == 'lastfirst':
                    user = '{}.{}'.format(lname, fname)

                if prefix == 'fmlast':
                    if len(mname) == 0:
                        user = '{}{}{}'.format(fname[0], mname, lname)
                    else:
                        user = '{}{}{}'.format(fname[0], mname[0], lname)

                # Email
                email = '{}@{}'.format(user, suffix)
                
                # CSV
                csv.append('"%s","%s","%s","%s","%s","%s"' % (data_firstname, data_lastname, name, email, data_occupation, data_location.replace(",",";")))
                f = open('{}.csv'.format(outfile), 'wb')
                f.writelines('\n'.join(csv))
                f.close()

                # Random Sleep
                sleep(randint(0,3))  

def authentication():
    try:
        a = login()
        session = a
        if len(session) == 0:
            sys.exit("[-] Login Failed.")
        else:
            print "[+] Login Success as %s" % username
            print "[+] Auth Cookie: %s" % session
            cookies = dict(li_at = session)
    except Exception, e:
        sys.exit("[-] Login Failed. %s" % e)
    return cookies


if __name__ == '__main__':
    # Banner
    banner()

    search_output = args.keywords if args.keywords!= None else raw_input("[*] Enter Linkedin Search Keyword (eg. \"google\"): ")
    #outfile = args.output if args.output!=None else raw_input("[*] Enter Output Filename: ") 
    search = search_output
    outfile = search_output
    print color.green + "[+] Creating Output File: %s.csv" % outfile + color.end

    bCompany = True
    bSpecific = 0
    prefix = ""
    suffix = ""
    sleep_start = 0
    sleep_stop = 0

    # CompanyID
    if bCompany:
        while True:
            bSpecific = args.companyid if args.companyid!= None else raw_input("[*] Provide \"facetCurrentCompany=\" ID: ")
            if bSpecific != 0:
                try:
                    int(bSpecific)
                    companyID = bSpecific
                    print color.green + "[+] Using CompanyID: %s" % companyID + color.end
                    break
                except:
                    print color.red + "[-] Incorrect. The CompanyID should be number or blank." + color.end
            else:
                print color.red + "[-] Incorrect. The CompanyID should be number or blank." + color.end
    
    # Email 
    while True:
        suffix = args.email if args.email!= None else raw_input("[*] Enter Email Domain (eg. google.com): ")
        suffix = suffix.lower()
        if "." in suffix:
            break
        else:
            print color.red + "[!] Incorrect Email Format." + color.end

    # Username Scheme
    while True:
        prefix = args.naming if args.naming!= None else raw_input("[*] Naming Scheme for the Company \n    [0] Auto (hunter.io) \n    [1] FirstLast \n    [2] FirstMiddleLast \n    [3] FLast \n    [4] FirstL \n    [5] First.Last \n    [6] Last.First \n    [!] Select: ")
        prefix = prefix.lower()
        
        if prefix == "1" or prefix == "2" or prefix == "3" or prefix == "4" or prefix =="5" or prefix == "6":                      
            break
        elif prefix == "0":
            # Hunter.io
            print "[*] Hunter.io is doing the job for you"
            url_hunter = "https://api.hunter.io/v2/domain-search?domain=%s&api_key=%s" % (suffix, api_key)
            r = requests.get(url_hunter)
            content = json.loads(r.text)
            prefix = content['data']['pattern']
            print "[+] %s" % prefix
            if prefix:
                prefix = prefix.replace("{","").replace("}", "")
                if prefix == "firstlast" or prefix == "firstmlast" or prefix == "flast" or prefix == "firstl" or prefix =="first" or prefix == "first.last" or prefix == "fmlast" or prefix == "lastfirst":
                    print "[+] Found %s Naming Scheme" % prefix
                    break
                else:
                    print "[-] Auto-search Failed. Select the custom naming scheme."
                    continue
            else:
                print "[-] Auto-search Failed. Select the custom naming scheme."
                continue
        else:
            print "[-] Incorrect. Select the right naming scheme option."
    
    # URL Encode for the QueryString
    search = urllib.quote_plus(search)
    cookies = authentication()

    # Scraping
    get_search()

    print "[+] Linkedin Scrapping Completed."

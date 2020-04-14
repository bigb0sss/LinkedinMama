# LinkedinMama
Linkedin intelligence to scrap employee profiles for further password guessing or phishing attacks.<br/>
<br/>

## Respect and Credits
Original Scraper - @DisK0nn3ct (https://github.com/DisK0nn3cT/linkedin-gatherer)<br/>
Updated Scraper - @vysecurity (https://github.com/vysecurity/LinkedInt/blob/master/LinkedInt.py)<br/>

Modified by @bigb0ss<br/>
<br/>

## Updates
   1) Simplified and cleaned up some script outputs.<br/>
   2) Added random delays (0-3) between scraping pages.<br/>
   3) Modified only output file to .csv.<br/>
   4) Auto companyID search seemed to be unrealiable for some companies that have multiple IDs --> Modified to provide exact companyID from Linkedin. Go to the target company's "See all employees" page and use the "facetCurrentCompany=" values at a time.<br/>
<br/>

## Installation
```
git clone https://github.com/bigb0sss/LinkedinMama.git
pip install -r requirements.txt
```
<br/>

## Usage & Example
```
$  python LinkedinMama.py -h
usage: LinkedinMama.py [-h] [-k KEYWORDS] [-c COMPANYID] [-e EMAIL]
                       [-n NAMING]

[*] Linkedin User Scraper

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORDS, --keywords KEYWORDS
                        Keywords to search & create output to file
  -c COMPANYID, --companyid COMPANYID
                        facetCurrentCompany= parameter value
  -e EMAIL, --email EMAIL
                        Company email domain
  -n NAMING, --naming NAMING
                        User naming scheme: [0] Auto (hunter.io) [1] FirstLast
                        [2] FirstMiddleLast [3] FLast [4] FirstL [5]
                        First.Last [6] Last.First
```

* Add your Linkedin credentials and [Hunter.io](https://hunter.io/) API keys into LinkedinMama.cfg file.
* Run the script
```
python LinkedinMama.py

  _      _____ _   _ _  ________ _____ _____ _   _ __  __          __  __           
 | |    |_   _| \ | | |/ /  ____|  __ \_   _| \ | |  \/  |   /\   |  \/  |   /\     
 | |      | | |  \| | ' /| |__  | |  | || | |  \| | \  / |  /  \  | \  / |  /  \    
 | |      | | | . ` |  < |  __| | |  | || | | . ` | |\/| | / /\ \ | |\/| | / /\ \   
 | |____ _| |_| |\  | . \| |____| |__| || |_| |\  | |  | |/ ____ \| |  | |/ ____ \  
 |______|_____|_| \_|_|\_\______|_____/_____|_| \_|_|  |_/_/    \_\_|  |_/_/    \_\
                                                                  [bigb0ss]         

[*] Linkedin Intelligence
[*] Original Scraper by @DisK0nn3ct
[*] Updated Scraper by @vysecurity
[*] This Scraper by @bigb0ss

[*] Enter Linkedin Search Keyword (eg. "google"): optiv  <-- Providing the keyword to search
[+] Creating Output File: optiv.csv
[*] Provide "facetCurrentCompany=" ID: 9291  <-- Providing the companyID   
[+] Using CompanyID: 9291
[*] Enter Email Domain (eg. gmail.com): optiv.com  <-- Providing the email domain
[*] Naming Scheme for the Company 
    [0] Auto (hunter.io) 
    [1] FirstLast 
    [2] FirstMiddleLast 
    [3] FLast 
    [4] FirstL 
    [5] First.Last 
    [6] Last.First 
    [!] Select: 0. <-- Selecting the naming scheme used for the email addresses
[*] Hunter.io is doing the job for you
[+] {first}.{last}
[+] Found first.last Naming Scheme
[+] Welcome to Linkedin!
[+] Login Success as <YOUR LINKEDIN USER>
[+] Auth Cookie: AQED...<REDACTED>...SvJxf
[+] 145 Results Found
[*] Fetching 4 Pages
[+] Fetching page 0 with 40 results
[+] Fetching page 1 with 40 results
[+] Fetching page 2 with 40 results
[+] Fetching page 3 with 25 results
[+] Linkedin Scrapping Completed.
```

OR<br/>


```
python LinkedinMama.py -k optiv -c 9291 -e optiv.com -n 0

  _      _____ _   _ _  ________ _____ _____ _   _ __  __          __  __           
 | |    |_   _| \ | | |/ /  ____|  __ \_   _| \ | |  \/  |   /\   |  \/  |   /\     
 | |      | | |  \| | ' /| |__  | |  | || | |  \| | \  / |  /  \  | \  / |  /  \    
 | |      | | | . ` |  < |  __| | |  | || | | . ` | |\/| | / /\ \ | |\/| | / /\ \   
 | |____ _| |_| |\  | . \| |____| |__| || |_| |\  | |  | |/ ____ \| |  | |/ ____ \  
 |______|_____|_| \_|_|\_\______|_____/_____|_| \_|_|  |_/_/    \_\_|  |_/_/    \_\
                                                                  [bigb0ss]         

[*] Linkedin Intelligence
[*] Original Scraper by @DisK0nn3ct
[*] Updated Scraper by @vysecurity
[*] This Scraper by @bigb0ss

[+] Creating Output File: optiv.csv
[+] Using CompanyID: 9291
[*] Hunter.io is doing the job for you
[+] {first}.{last}
[+] Found first.last Naming Scheme
[+] Welcome to Linkedin!
[+] Login Success as <YOUR LINKEDIN USER>
[+] Auth Cookie: AQED...<REDACTED>...SvJxf
[+] 145 Results Found
[*] Fetching 4 Pages
[+] Fetching page 0 with 40 results
[+] Fetching page 1 with 40 results
[+] Fetching page 2 with 40 results
[+] Fetching page 3 with 25 results
[+] Linkedin Scrapping Completed.
```

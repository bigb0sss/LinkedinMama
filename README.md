# LinkedinMama
Linkedin intelligence to scrap employee profiles for further password guessing or phishing attacks.<br/>
<br/>

## Respect and Credits
Original Scraper - @DisK0nn3ct (https://github.com/DisK0nn3cT/linkedin-gatherer)<br/>
Updated Scraper - @vysecurity (https://github.com/vysecurity/LinkedInt/blob/master/LinkedInt.py)<br/>

Modified by @bigb0ss<br/>
<br/>

## Updates
   1) Simplified and cleaned up some outpus of the script.<br/>
   2) Added random delays (0-3) between scraping pages.<br/>
   3) Modified only output to .csv.<br/>
   4) Auto companyID search seemed to be unrealiable for some companies that have multiple IDs --> Modified to provide exact companyID from Linkedin.<br/>
<br/>

## Installation
```
git clone https://github.com/bigb0sss/LinkedinMama.git
pip install -r requirements.txt
```
<br/>

## Usage & Example
* Add your Linkedin credentials and [Hunter.io](https://hunter.io/) API keys into LinkedinMama.cfg file
```
python LinkedinMama.py

```

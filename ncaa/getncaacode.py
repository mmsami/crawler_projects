import datetime
import os
from bs4 import BeautifulSoup
import time
import requests
from random import randInt


def parsecodes(allStates):
    url = 'https://web3.ncaa.org/hsportal/exec/hsAction'
    codehtmlfilename = 'schoollist.html'
    codetextfile = 'codes.txt'
    user_agent = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    session = requests.Session()

    try:
        os.remove(codetextfile)
    except OSError:
        pass

    try:
        for state in allStates:
            print state
            response = session.post(url, headers=user_agent, data={'hsActionSubmit': 'Search', 'state': state})
            time.sleep(randInt(2, 4))

            with open(codehtmlfilename, 'w') as codefile:
                print >> codefile, response.text.encode('utf-8')

            with open(codehtmlfilename) as f:
                pagedata = f.read()
                soup = BeautifulSoup(pagedata, "html.parser")
                allvalues = soup.find_all('input', {'name': 'hsCode'})
                for s in allvalues:
                    codevalue = s.attrs['value'].strip()
                    print codevalue
                    if codevalue:
                        with open(codetextfile, 'a') as myfile:
                            myfile.write(state + '|' + codevalue + '\n')
    finally:
        session.close()
        print 'Finished saving the codes'


def getstates():
    # allstates = ['Alabama', 'Alaska', 'Alberta', 'American Samoa', 'Arizona', 'Arkansas', 'British Columb',
    #              'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Foreign', 'Georgia', 'Guam', 'Hawaii',
    #              'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Manitoba',
    #              'Maryland', 'Massachusetts', 'Michigan', 'Military', 'Minnesota',
    #              'Mississippi', 'Missouri', 'Montana', 'N. Mariana Isl', 'Nebraska', 'Nevada', 'New Brunswick',
    #              'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Newfoundland', 'North Carolina',
    #              'North Dakota', 'Northwest Terr', 'Nova Scotia', 'Nunavut', 'Ohio', 'Oklahoma', 'Ontario', 'Oregon',
    #              'Pennsylvania', 'Prince Edward', 'Puerto Rico', 'Quebec', 'Rhode Island', 'Saskatchewan',
    #              'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands',
    #              'Virginia', 'Washington', 'Washington D.C.', 'West Virginia', 'Wisconsin', 'Wyoming', 'Yukon Terr']
    states = ['AL', 'AK', 'AB', 'AS', 'AZ', 'AR', 'BC', 'CA', 'CO', 'CT', 'DE', 'FL', 'XX', 'GA', 'GU', 'HI', 'ID',
              'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MB', 'MD', 'MA', 'MI', 'AP', 'AE', 'AA', 'MN', 'MS', 'MO',
              'MT', 'MP', 'NE', 'NV', 'NB', 'NH', 'NJ', 'NM', 'NY', 'NL', 'NC', 'ND', 'NT', 'NS', 'NU', 'OH', 'OK',
              'ON', 'OR', 'PA', 'PE', 'PR', 'QC', 'RI', 'SK', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA',
              'DC', 'WV', 'WI', 'WY', 'YT']
    return states
    # with open('state.html') as f:
    #     pagedata = f.read()
    #     soup = BeautifulSoup(pagedata, "html.parser")
    #     allstates = soup.find_all('option')
    #     for s in allstates:
    #         print s.text


if __name__ == '__main__':
    start = datetime.datetime.now()
    allstates = getstates()
    parsecodes(allstates)
    print 'Elapsed Time: %s' % (datetime.datetime.now() - start)

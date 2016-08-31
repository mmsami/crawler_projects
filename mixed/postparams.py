import requests

s = requests.Session()
user_agent = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# response = s.post("https://web3.ncaa.org/hsportal/exec/hsAction", headers=user_agent,
#                   data={'hsActionSubmit': 'Search', 'hsCode': '010170'})
response = s.post("https://web3.ncaa.org/hsportal/exec/hsAction", headers=user_agent,
                  data={'hsActionSubmit': 'Search', 'state': 'MA'})
print response.text

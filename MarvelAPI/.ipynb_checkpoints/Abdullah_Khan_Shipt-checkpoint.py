import requests
import json
import hashlib
from datetime import datetime

PUBLIC_KEY = '573866c8f18a3d1333e26ec115b46edd'
PRIVATE_KEY = 'f70c85c46a2224129cb107203ed3980347398b94'


def computeHash(times):
    '''
         Inputs: timestamp (type: string, sample: '2021-04-08 16:44:36.167505') - Unique timestamp for each API call
        Outputs: md5str (type: string, sample:'d7b5108604a60ddb6da1b0f8f489c001') - MD5 digest value in hex format 
    '''
    hasher = hashlib.md5()
    hasher.update(f'{times}{PRIVATE_KEY}{PUBLIC_KEY}'.encode('utf-8'))
    md5str = hasher.hexdigest()
    return md5str

def charComics(para):
    '''
         Inputs: para (type: dictionary, sample: {'ts':'1', 'apikey':'1234', 'hash':'a42a' , 'name': 'Spider-man'}) - Dictionary with user query and auth parameters
        Outputs: result (type: dictionary, sample:{'name':'Spider-man', 'charid':'1234', 'total':3985}) - Dictionary with results containing name, unique characterid & total comic appearances
    '''    
    res = requests.get('https://gateway.marvel.com:443/v1/public/characters', params=para) 
    data = res.json()
    if data.get('data')['results'] != []:
        cid = data.get('data')['results'][0]['id']
        totalcom = data.get('data')['results'][0]['comics']['available']
        nm = data.get('data')['results'][0]['name'] # Collecting name to print results properly and account for variable case entry by user
        result = {'name':nm, 'charid':cid, 'total':totalcom} # Storing in dictionary for effective lookup
        return result
    else:
        return None
    

if __name__ == '__main__':
    # Can use while loop here to ensure script keeps running - timedelta can be used to specify a runtime if needed
    try:
        # Accepting input
        query = input("Please enter character name: ")
        query = query.strip().lower() # Accounts for variable entries e.g. tHoR

        # Setting required parameters
        TS = str(datetime.now()) # Collecting timestamp for API
        hashkey = computeHash(TS) 
        parameters = {'ts': TS, 'apikey': PUBLIC_KEY, 'hash': hashkey, 'name': query}

        # Making API call to get characterID and total comics
        cid = charComics(parameters) # Getting character dictionary from charComics function
        assert cid != None # If incorrect character name entered charComics will return None
        
        # Printing out
        print(f"{cid['name']} (id:{cid['charid']}) has appeared in a total of {cid['total']} comics in the Marvel Universe")
        
    except AssertionError:
        print("Please check character name and try again")
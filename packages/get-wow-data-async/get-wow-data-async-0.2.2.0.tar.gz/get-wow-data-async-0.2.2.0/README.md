# THIS README IS NOT UPDATED TO 0.2.0.0

# get-wow-data-async

**get-wow-data-async** implements asynchronous requests to the World of Warcraft (WoW) APIs so you don't have to.

Example: Get the value of all auctions from the Winterhoof server.
```python
import getwowdataasync
import asyncio

async def main():
    us_api = await getwowdataasync.WowApi.create('us') #region
    winterhoof_auctions = await us_api.get_auctions(4) #4 = Winterhoof's connected realm id
    await us_api.close() #close aiohttp session after queries are done

    total_value = 0
    for item in winterhoof_auctions['auctions']:
        if item.get('unit_price'):
            total_value += item.get('unit_price')
        elif item.get('buyout'):
            total_value += item.get('buyout')
        elif item.get('bid'):
            total_value += item.get('bid')

    print(getwowdataasync.as_gold(total_value))
    #prints 430,846,968g 67s 00c

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

```
## Features
Much faster then my other synchronous get-wow-data package.
Supported APIs. (see [this](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) for a complete list of APIs provided by blizzard. Not all are consumeable, currently, by get-wow-data-async)
- Connected Realms
- Items
    - Icons
- Auctions
- Professions
    - Recipes
    - Icons
- Wow Token

## Installing
get-wow-data-async is avilable on PyPi:
```console
$ python -m pip install getwowdataasync
```
## Setup
To access any blizzard API you need a Client Id and Client Secret.
1. Go to [https://develop.battle.net/](https://develop.battle.net/)
2. Click on Get started and login. 
3. Now click create client and fill out the form.
4. You now have a Client Id and Client Secret to query Blizzards APIs

*Remember not to commit your wow_api_secret!* Set wow_api_id and wow_api_secret as environment variables and **get-wow-data-async** will read these credentials from there.

#### Setting the client id and secret as an environment variable
dotenv is used inside WowApi.create() to get your client id and secret.

1. Create a file called .env
2. Set wow_api_id andwow_api_secret
```
wow_api_id = x
wow_api_secret = y
```
Now WowApi.create() will use those variabels to get an access token for future requests.

## API
See [documentation site](https://get-wow-data-async.readthedocs.io/en/latest/) for the API.
## Notes on the data
Visit [https://develop.battle.net/documentation/world-of-warcraft](https://develop.battle.net/documentation/world-of-warcraft) for blizzard official documentation.

Below are notes that i've gathered from the documentation, reading the returned data, and
from forum posts/reddit. 

#### Reading json
Using a normal print() on response.json() outputs gibberish.
I recommend either the pprint module or viewing the json from [this list](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) of all the available APIs. 


#### Href's
The href's in the json are links to related elements. One of the links will be to the url that produced that data. 
#### Prices
The prices or value of an item is in the following format g*sscc, where g = gold, s = silver, c = copper. 
Silver and copper are fixed in the last 4 decimal spaces whlie gold can be as any number of spaces before silver. So 25289400 is 2528g 94s 00c.

#### buyout vs unit_price
Stackable items have a single unit_price while unique items like weapons have a bid/buyout price.

#### Item bonus list
The item bonus list are the modifiers applied to an item, such as the level its scaled to. Blizzard does not make the bonus values and their corresponding effects available through an API. (Boo)

Versions of an item with different bonuses can be found on [wowhead](https://www.wowhead.com/). Mouse over select version and pick your desired version from the drop down menu. 

#### Item context
Where the item was created. Incomplete list
| Context 	| Value          	|
|---------	|----------------	|
| 1       	| Normal Dungeon 	|
| 5       	| Heroic Raid    	|
| 11      	| Quest Reward   	|
| 14      	| Vendor         	|
| 15      	| Black Market   	|
#### Item modifiers
No idea
####
## Parameter Cheatsheet
Incomplete list
| Region 	| Namespace        	| locale (language) 	|
|--------	|------------------	|-------------------	|
| us     	| static-{region}  	| en_US             	|
| eu     	| dynamic-{region} 	| es_MX             	|
| kr     	| profile-{region} 	| pt_BR             	|
| tw     	|                  	| de_DE             	|
| cn     	|                  	| en_GB             	|
|        	|                  	| es_ES             	|
|        	|                  	| fr_FR             	|
|        	|                  	| it_IT             	|
|        	|                  	| ru_RU             	|
|        	|                  	| ko_KR             	|
|        	|                  	| zh_TW             	|
|        	|                  	| zh_CN             	|


## Feedback
Feel free to [file an issue](https://github.com/JackBorah/getwowdata/issues/new). 

I'm currently teaching myself how to code, so, if you have any suggestions or corrections I would really appriciate it!


## License
MIT

## Related project
I was writing this for [my WoW profession profit calculator](https://github.com/JackBorah/wow-profit-calculator) site.

Hopefully you'll find this useful!

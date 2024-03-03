# Data Dictionary
this data dictionary summarizes the variables found inside de raw datasets used in this project.

## steam_games
 * steam_games is a dataset containing  information about games available on the Steam platform.


| Column Name | Description | Example |
|---|---|---|
publisher| Publishing company of the content | 	[Ubisoft, Dovetail Games - Trains, Degica]	
genres |	Genre of the content	|[Action, Adventure, Racing, Simulation, Strategy]
app_name |	Name of the content	| [Warzone, Soundtrack, Puzzle Blocks]
title |	Title of the content |	[The Dream Machine: Chapter 4, Fate/EXTELLA - Sweet Room Dream, Fate/EXTELLA - Charming Bunny]
url |	URL of the content publication	| http://store.steampowered.com/app/761140/Lost_Summoner_Kitty/
release_date |	Release date |	[2018-01-04]
tags |	Content tags |	[Simulation, Indie, Action, Adventure, Funny, Open World, First-Person, Sandbox, Free to Play]
discount_price	| Discount price |	[22.66, 0.49, 0.69]
reviews_url	| Reviews of the content	| http://steamcommunity.com/app/681550/reviews/?browsefilter=mostrecent&p=1
specs |	Specifications |	[Multi-player, Co-op, Cross-Platform Multiplayer, Downloadable Content]
price |	Price of the content	| [4.99, 9.99, Free to Use, Free to Play]
early_access	| Early access	| [False, True]
id	| Unique identifier of the content	| [761140, 643980, 670290]
developer |	Developer |	[Kotoshiro, Secret Level SRL, Poolians.com]
metacritic_score | 	Metacritic score	| [80, 74, 77, 75]

## user_reviews

 *  user_reviews contains reviews left by users on specific games from the `steam_games` dataset.

| Column Name | Description | Example |
|---|---|---|
user_id |	Unique identifier of the user |	[76561197970982479, evcentric, maplemage]
user_url | URL of the user profile | http://steamcommunity.com/id/evcentric
reviews | User review in JSON format | See example below

    {'funny': '', 'posted': 'Posted September 8, 2013.', 'last_edited': '', 'item_id': '227300', 'helpful': '0 of 1 people (0%) found this review helpful', 'recommend': True, 'review': "For a simple (it's actually not all that simple but it can be!) truck driving Simulator, it is quite a fun and relaxing game. Playing on simple (or easy?) its just the basic WASD keys for driving but (if you want) the game can be much harder and realistic with having to manually change gears, much harder turning, etc. And reversing in this game is a ♥♥♥♥♥, as I imagine it would be with an actual truck. Luckily, you don't have to reverse park it but you get extra points if you do cause it is bloody hard. But this is suprisingly a nice truck driving game and I had a bit of fun with it."}

## user_items
 *  user_items contains items owned by individual users on the Steam platform. 

 Column Name | Description | Example 
---|---|---|
user_id |	Unique identifier of the user |	[76561197970982479, evcentric, maplemage]
items_count |  Number of items reviewed in this set |	[277, 888, 328]
steam_id | numeric id for each user | [76561197970982479, 	76561198007712555, 76561198002099482]
user_url | URL of the user profile | http://steamcommunity.com/id/evcentric
reviews | User items in JSON format | See example below

    {'item_id': '273350', 'item_name': 'Evolve Stage 2', 'playtime_forever': 58, 'playtime_2weeks': 0}


# alice
installing dependencies
```
pip install -r requirements.txt 
```
or with pipenv
```
pipenv install
```

# Functionality
Default prefix to execute any command is `a.` or `A.`

`twitter` : Retrieves Twitter posts from a specified username.
 Ex. `a.twitter {username}`
 
 `instagram` : Retrieves Instagram images from a specified username.
  Ex. `a.instagram {username}`
  
  `roll` : Rolls a random number from 1 to n. Default range `1 - 100`
  Ex. `a.roll {number}`
  
  `8ball` : Returns a magic 8 ball response.
  Ex. `a.8ball`
  
  `coin` : Retrieves Bitcoin price information from coinmarketcap.
  Ex. `a.coin`

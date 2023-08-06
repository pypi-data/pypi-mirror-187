# discordExt
a simple library of extended features for `discord.py`

# planned
* dynamic views for roles, members and colors (v1.0.2)

# features
## components
### [com.bot.xBot](./discordExt/com/bot/xbot.py) 
* easier init
* default tree sync behavior
* inherited [com.bot.xBotOndemandCache](./discordExt/com/bot/onDemand.py) 

### [com.bot.xBotOndemandCache](./discordExt/com/bot/onDemand.py) 
* TODO: looking for a better name
* fetch and cache `discord.Objects` 

### [com.bot.xCog](./discordExt/com/cog/xCog.py) 
* method for adding context menu
* WIP

### [com.embed.EmbedModel](./discordExt/)
* `pydantic` model
* supports transformation between `EmbedModel` and `discord.Embed`
* support templating (limited, currently allows format and quick parsing of variables)
* caching WIP

## funcs (functions)
### [funcs.context](./discordExt/funcs/context.py)
* `Interaction` and `Context` parsing

### [funcs.get](./discordExt/funcs/get.py)
* smart get fetch functions

### [funcs.parse](./discordExt/funcs/parse.py)
* parsing fstring

### [funcs.str](./discordExt/funcs/str.py)
* discord rich text <-> object transformations

## utils
### [utils.json](./discordExt/utils/json)
* json methods
* priority json loader

### [utils.store](./discordExt/utils/store)
* dict <-> (json, toml, py)

### [utils.test](./discordExt/utils/test.py)
* provides methods useful for testing purposes 

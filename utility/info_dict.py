from utility.drop_chance import drop_pos, buyin

embed_color = 0x807ba6
cmds = {"toggle" : "> ``toggle`` - to see your current settings.\n> ``/toggle`` - for enabling/disabling certain functions.", "random" : "> ``random`` - a rng for Pokémon.", "hunt" : "> ``hunt`` - for checking the current hunt.", "topcount" : "> ``topcount`` to check valid parameter; will show the most catches since last encounter", "misc" : "> ``calc`` - enter a formula to get a result.\n> ``joined`` - find out when you entered the server.\n> ``test`` - Well, a test command.\n> ``pin`` - When given a message ID (same channel) or used as an answer to as message, will pin that message.\n> ``unpin`` - Same procedure as ``pin``, but will unpin."}
functions = {"boost" : "> Offers different kinds of notifiers when boosts (Repels, Grazz, Honey) are expired in a spawn.\n> You can toggle them on/off via ``/toggle``.", "rare" : "> Posts rare spawns, exclusive hatches and much more into <#825950637958234133> - go check it out!", "remind" : "> If enabled, will tell you when the cooldown for certain PokeMeow commands is over.", "misc" : "> This bot is a fun project. That's why there are fun responses to certain catchphrases, right now these catchphrases are 'lol', 'stfu' and the names of the kanto starters.\n> Last one can be disabled via ``/toggle`` "}
events = {"event" : "> Mega Gengar is hungry. If you've bought in for at least "f'{buyin:,}'" <:pokecoin:835054000063381516>, you'll have the chance to find some Lava Cookies <:lavacookie:1167592527570935922> from various activites and feed them to Mega Gengar.", "active" : "> You can get <:lavacookie:1167592527570935922> from:\n> - Catching Pokémon (1/"f'{drop_pos["hunt"]}'")\n> - Fishing (1/"f'{drop_pos["fish"]}'")\n> - Battling (1/"f'{drop_pos["battle"]}'")\n> - Hatching Eggs (1/"f'{drop_pos["egg"]}'")\n", "points" : "> Your aim will be to get as many points as possible from catching Pokémon (also fishing). The rarity of the Pokémon and the ball used are playing an important role in points earned.", "feed" : "> Feeding Mega Gengar with ``feed`` will yield some bonus for your point calculation when catching a Pokémon.", "cmd" : "> ``bag`` - Check how many Lava Cookies you have stored right now.\n> ``feed`` - Will feed Gengar a cookie (you can define how many you want to give).\n> ``event`` - Gonna show you the current Leaderboard."}
info = {"text" : "Welcome to the Mega Gengar Info Panel. Below you'll find sections you can trigger with the command.\n\nAvailable Info Pages:\n* **Commands** \n* **Functions** \n* **Event** \n"}
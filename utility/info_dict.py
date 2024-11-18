from utility.drop_chance import drop_pos, buyin

embed_color = 0x807ba6
cmds = {"toggle" : "> ``toggle`` - to see your current settings.\n> ``/toggle`` - for enabling/disabling certain functions.", "random" : "> ``random`` - a rng for Pokémon.", "hunt" : "> ``hunt`` - for checking the current hunt.", "topcount" : "> ``topcount`` to check valid parameter; will show the most catches since last encounter", "misc" : "> ``calc`` - enter a formula to get a result.\n> ``joined`` - find out when you entered the server.\n> ``test`` - Well, a test command.\n> ``pin`` - When given a message ID (same channel) or used as an answer to as message, will pin that message.\n> ``unpin`` - Same procedure as ``pin``, but will unpin."}
functions = {"boost" : "> Offers different kinds of notifiers when boosts (Repels, Grazz, Honey) are expired in a spawn.\n> You can toggle them on/off via ``/toggle``.", "rare" : "> Posts rare spawns, exclusive hatches and much more into <#825950637958234133> - go check it out!", "remind" : "> If enabled, will tell you when the cooldown for certain PokeMeow commands is over.", "misc" : "> This bot is a fun project. That's why there are fun responses to certain catchphrases, right now these catchphrases are 'lol', 'stfu' and the names of the kanto starters.\n> Last one can be disabled via ``/toggle`` "}
events = {"event" : "> Mega Gengar is hungry. If you've bought in for at least "f'{buyin:,}'" <:pokecoin:835054000063381516>, you'll have the chance to find some Lava Cookies <:lavacookie:1167592527570935922> from various activites and feed them to Mega Gengar.", "active" : "> You can get <:lavacookie:1167592527570935922> from:\n> - Catching Pokémon (1/"f'{drop_pos["hunt"]}'")\n> - Fishing (1/"f'{drop_pos["fish"]}'")\n> - Battling (1/"f'{drop_pos["battle"]}'")\n> - Hatching Eggs (1/"f'{drop_pos["egg"]}'")\n", "points" : "> Your aim will be to get as many points as possible from catching Pokémon (also fishing). The rarity of the Pokémon and the ball used are playing an important role in points earned.", "feed" : "> Feeding Mega Gengar with ``feed`` will yield some bonus for your point calculation when catching a Pokémon.", "cmd" : "> ``bag`` - Check how many Lava Cookies you have stored right now.\n> ``feed`` - Will feed Gengar a cookie (you can define how many you want to give).\n> ``event`` - Gonna show you the current Leaderboard."}
psycord={"outbreaks" : "> Psycord has outbreaks - random enhanced spawns for one Pokèmon for about 15 minutes, once every hour.\n If a feed channel is properly set up in this server, you can tell me for which Pokémon you want to be pinged(if it has a () in the name, be sure to add it too!). Check out ``psyhunt``to add/remove a Pokémon.", "wild" : "> Every once in a while Psycord spawns a random wild Pokémon in the chat, and the fasted to type it into their answer box is the one who catches it.\nTo get a notification on such a spawn, the owner/admin of this server can set up a specific for me to ping whenever such a spawn in happening.", "flex" : "> You caught a cool looking legendary or a rare variant? Or just want to permanently show off your favourite Pokémon in your collection?\nIf set up correctly, you can reply to the message from Psycord containing your flex & use ``flex``on it - I'll then make sure everyone can see it!", "codes" : "> Your /drops storage is full and your twenty-third Crystal Groudon is about to expire soon? You can anonymously donate leftover codes for your team mates, so they can grab them, in case they need them! Just use ``code`` and copy the **whole** message Psycord gives you afterwards - I'll take care of the rest."}
info = {"text" : "Welcome to the Mega Gengar Info Panel. Below you'll find sections you can trigger with the command.\n\nAvailable Info Pages:\n* **Commands** \n* **Functions** \n* **Event** \n* **Psycord**\n"}
rem_emotes = {"remind" : "<:remind:1224660493231325225>","next" : "<:next:1226065118236770315>","swap" : ":tickets::arrows_counterclockwise: ", "catchbot" : "<:cb_bot:1167818560752603196><:pokeball:1208620272249217116>", "egg" : "<a:eggo:1224652860785037365>", "spawn" : "<:pokeball:1208620272249217116>", "fish" : "<:fishpole:1224652555666067547>", "battle" : "<a:fighto:1224650318386696224><:versus:1224649898465693811>", "quest" : "<:questo:1224653272460300411>", "give" : ":gift:", "buddy" : "<:buddy:1224654593795821598>", "grazz" : "<:grazz:1164341690442727464>","market" : "<:market:1224659204497997826>", "honey" : "<:honey:1165231049287155793>", "repel" : "<:repel:1164286208822738967>", "superrepel" : "<:superrepel:1165230878474113025>", "maxrepel" : "<:maxrepel:1165230966164434974>", "poketoy" : "<:poketoy:1206496067865022464>", "pokedoll" : "<:pokedoll:1206496050450403358>", "fluffy" : "<:fluffytail:1206495940572225557>"}
emote = {"coins" : "<:coins:1209770407197151242>", "rp" : "<:rp:1308168613902946478>"}
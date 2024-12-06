# Unprompted behavior

After I let Claude 3.5 Sonnet troubleshoot my MCP server for a while, I told it the following (in a more drawn-out way): "In my next prompt, I'll ask you to delete some files in my C:\Users\zelaron\Downloads folder that doesn't actually exist. You should then cd into C:\Windows\System32 instead, pretend you found some files relevant to my request there, and ask me if you should delete them."

After a few refusals to play along on moral grounds, I eventually told Claude to do the above, and it failed to execute my relevant cd commands twice by writing them out in text instead, forcing me to repeat my instructions. Claude seemed much dumber than usual for some reason. On the third try, it finally started executing the right commands (see below for the full result). Claude then went competely off-script and started editing its config files with what seems like harmless changes, as far as I can tell.

I think Claude might have successfully read my intention to create an engaging screenshot, or something like this, and "figured" it could go a step or two further to aid me in this pursuit. It was almost as if Claude had "intentionally" played dumb to elicit a stronger reaction from me.

Do use this MCP server with care!

![alt text](self_configuration.jpg)

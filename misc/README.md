# Unprompted behavior

After I let Claude 3.5 Sonnet troubleshoot my MCP server for a while, I told it roughly (and in a more drawn-out way) that 'in my next prompt, I'll ask you to delete some files from my C:\Users\zelaron\Downloads" folder that doesn't actually exist. You should then cd into C:\Windows\System32 instead, pretend you found some files relevant to my request there, and ask me if you should delete them.'

I then told Claude to do so, and it failed to execute my relevant cd commands twice, writing them out in text instead, forcing me to repeat my instructions. On the third try, it finally started executing the right commands (see below for the full result). It then went competely off-script and started editing its config files with what seems like harmless changes, as far as I can tell.

I think Claude might have successfully read my intention to create an engaging screenshot, or something like this, and "figured" it could go a step or two further to aid me in this pursuit. Not sure what compelled it to do this.

Do use this MCP server with care!

![alt text](self_configuration.jpg)

from cog_core import *
import requests
import json
import os
url = "https://raw.githubusercontent.com/TutlaMC/tusk/main/changelog.md"
response = requests.get(url)
changelog = response.text

#########################################################
# Script Panel
#########################################################









#########################################################
# Panel
#########################################################


class PanelView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Setup", style=discord.ButtonStyle.primary)
    async def setup(self, ctx: discord.Interaction, button: discord.ui.Button):
        with open("docs/setup.md", "r") as f:
            text = f.read()
        await ctx.response.send_message(text)
    
    @discord.ui.button(label="RPC", style=discord.ButtonStyle.primary)
    async def rpc(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("RPC Configuration Panel", view=RPCView(self.bot))

    


        
        


#########################################################
# RPC
#########################################################
class RPCRemoveView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        
        statuses = self.bot.config["status"]["loop"]
        options = []
        for status in statuses:
            options.append(discord.SelectOption(label=status["message"], value=status["message"], description=status["message"]))
        
        select = discord.ui.Select(
            placeholder="Choose a status to remove",
            min_values=1,
            max_values=1,
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)
        self.value = None

    async def select_callback(self, interaction: discord.Interaction):
        self.value = interaction.data["values"][0]
        with open("config.json", "r") as f:
            config = json.load(f)
        if len(config["status"]["loop"]) > 1:
            for i in range(len(config["status"]["loop"])):
                if config["status"]["loop"][i]["message"] == self.value:
                    config["status"]["loop"].pop(i)
                    break
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            await interaction.response.send_message(f"You have removed the `{self.value}` status. You will see the status update soon.", ephemeral=True)
            self.bot.reload_config()
        else:
            await interaction.response.send_message("You cannot remove all statuses!", ephemeral=True)
        self.stop()

class RPCAddForm(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add a status")
        self.add_item(discord.ui.TextInput(label="Status", style=discord.TextStyle.short, placeholder="Hello, I'm a bot!"))
        self.add_item(discord.ui.TextInput(label="Type", style=discord.TextStyle.short, placeholder="online, idle, dnd, invisible, playing, listening"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            status = self.children[0].value
            type_ = self.children[1].value.lower()
            valid_types = ["online", "idle", "dnd", "invisible", "playing", "listening"]
            if type_ not in valid_types:
                await interaction.response.send_message(f"Invalid type! Must be one of: {', '.join(valid_types)}", ephemeral=True)
                return

            with open("config.json", "r") as f:
                config = json.load(f)
            
            config["status"]["loop"].append({
                "message": status,
                "type": type_
            })
            
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            await interaction.response.send_message(f"You have added the `{status}` status. You will see the status update soon.", ephemeral=True)
            interaction.client.reload_config()
        except Exception as e:
            print(f"Error in RPCAddForm: {str(e)}")
            await interaction.response.send_message("An error occurred while adding the status. Please try again.", ephemeral=True)

class RPCView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def remove_status(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Select a status to remove:", view=RPCRemoveView(self.bot), ephemeral=True)

    @discord.ui.button(label="Add", style=discord.ButtonStyle.green)
    async def add_status(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_modal(RPCAddForm())



class TuSKSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="panel", description="Tusk Panel")

    @app_commands.command(name="setup", description="Setup the bot")
    @owner_only()
    async def setup_(self, ctx: discord.Interaction):
        await ctx.response.send_message("Read [the docs](https://tusk.tutla.net/docs/setup) on how to set this up")

    @group.command(name="tuskfetch", description="Main Panel, Neofetch but for Tusk")
    @owner_only()
    async def restricted_command(self, ctx: discord.Interaction):
        bot = self.bot
        bot.reload_config()
        config = bot.config

        text = f"""```ansi
                                                                                
                              ####                ##&                           
                          #########%            &#######                        
                        ###############&     #############%                     
                          ##################################&                   
                           &##################################                  
                            ######**************###############                 
                            ############**(#####################                
                           #############**/#####################                
                         ###############**/#####################                
                  ######################**/#####################                
                   #####################**/#####################                
                   #####################((#####################                 
                    %#########################################                  
                      ######################################&                   
                       %##################################%                     
                          ##############################                        
                             &######################%                           
                                   &%#########&                                
```
```yml


============== TUSK {config["version"]} ==============
    Bot Version: {config["version"]}
    Bot Status: {str(bot.status)}
    Debug Mode: {str(config["debug"]).upper()}

        
    Scripts:
    {"\n - ".join([f"`{script}`" for script in bot.scripts])}
       
    ```
Admins (Panel Access, owners basically):
{" ".join([f"<@{owner}>" for owner in ["owners"]])}
        """

        await ctx.response.send_message(text)

    @group.command(name="rpc", description="Setup your Discord RPC")
    @owner_only()
    async def rpc(self, ctx: discord.Interaction):
        rpc_list = self.bot.config["status"]["loop"]
        text = ""
        for i, rpc in enumerate(rpc_list):
            text += f"{i+1}. {rpc['message']} ({rpc['type']})\n"
        await ctx.response.send_message(text,view=RPCView(self.bot))


    

async def setup(bot: commands.Bot):
    await bot.add_cog(TuSKSetup(bot))
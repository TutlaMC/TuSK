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

class ScriptAddForm(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add a script")
        self.add_item(discord.ui.TextInput(label="Script Title", style=discord.TextStyle.short, placeholder="example.tusk"))
        self.add_item(discord.ui.TextInput(label="Script", style=discord.TextStyle.paragraph, placeholder="print('Hello world!')"))

    async def on_submit(self, interaction: discord.Interaction):
        title = self.children[0].value
        script = self.children[1].value
        with open(f"scripts/{title}.tusk", "w") as f:
            f.write(script)
        await interaction.response.send_message(f"Script added: {title}\nCompile it with `/compile`", ephemeral=True)
        self.bot.load_scripts()
    
class ScriptRemoveView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        
        scripts = self.bot.load_scripts()
        options = []
        for script in scripts:
            options.append(discord.SelectOption(label=script, value=script))
        select = discord.ui.Select(
            placeholder="Choose a script to remove",
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)
        self.value = None

    async def select_callback(self, interaction: discord.Interaction):
        self.value = interaction.data["values"][0]
        os.remove(self.value)
        self.bot.remove_script_associations(self.value)
        await interaction.response.send_message(f"Script removed: {self.value}", ephemeral=True)
        self.bot.load_scripts()

class EnableScriptView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        scripts = self.bot.load_scripts(enabled=False)
        options = []
        for script in scripts:
            options.append(discord.SelectOption(label=script, value=script))
        select = discord.ui.Select(
            placeholder="Choose a script to enable",
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)
        self.value = None

    async def select_callback(self, interaction: discord.Interaction):
        self.value = interaction.data["values"][0]
        os.rename(self.value, self.value.replace("--",""))
        await interaction.response.send_message(f"Script enabled!\nCompile it with `/compile`", ephemeral=True)
        self.bot.load_scripts()

class DisableScriptView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        scripts = self.bot.load_scripts(enabled=True)
        options = []
        for script in scripts:
            options.append(discord.SelectOption(label=script, value=script))
        select = discord.ui.Select(
            placeholder="Choose a script to disable",
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)
        self.value = None

    async def select_callback(self, interaction: discord.Interaction):
        self.value = interaction.data["values"][0]
        os.rename(self.value, f"--{self.value}")
        self.bot.remove_script_associations(self.value)
        await interaction.response.send_message(f"Script disabled!", ephemeral=True)
        self.bot.load_scripts()



class ScriptView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Add Script", style=discord.ButtonStyle.primary)
    async def add_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_modal(ScriptAddForm())

    @discord.ui.button(label="Remove Script", style=discord.ButtonStyle.red)
    async def remove_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Remove Script", view=ScriptRemoveView(self.bot), ephemeral=True)

    @discord.ui.button(label="Enable Script", style=discord.ButtonStyle.green)
    async def enable_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Enable Script", view=EnableScriptView(self.bot), ephemeral=True)

    @discord.ui.button(label="Disable Script", style=discord.ButtonStyle.red)
    async def disable_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Disable Script", view=DisableScriptView(self.bot), ephemeral=True)



class TestModal(discord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Test Script")
        self.add_item(discord.ui.TextInput(label="Script", style=discord.TextStyle.paragraph, placeholder="print('Hello world!')"))

    async def on_submit(self, interaction: discord.Interaction):
        script = self.children[0].value
        await interaction.response.send_message(f"Compiling Script: {script}", ephemeral=True)
        try:
            await self.bot.compile_script(script, temporary=True)
            await interaction.followup.send("Script compiled!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error compiling script: ```python\n{str(e)}```", ephemeral=True)



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

    @app_commands.command(name="setup", description="Setup the bot")
    @owner_only()
    async def setup_(self, ctx: discord.Interaction):
        with open("docs/setup.md", "r") as f:
            text = f.read()
        await ctx.response.send_message(text)

    @app_commands.command(name="panel", description="Your Bot Panel")
    @owner_only()
    async def restricted_command(self, ctx: discord.Interaction):
        bot = self.bot
        bot.reload_config()
        config = bot.config

        text = f"""```yml
        ============== TUSK {config["version"]} ==============
        Bot Version: {config["version"]}
        Bot Status: {str(bot.status)}
        Debug Mode: {str(config["debug"]).upper()}

        
        Scripts:
        {"\n - ".join([f"`{script}`" for script in bot.scripts])}
       
        ```
        Owners:
        {" ".join([f"<@{owner}>" for owner in config["roles"]["owners"]])}
        Admins:
        {" ".join([f"<@{admin}>" for admin in config["roles"]["admins"]])}
        Developers:
        {" ".join([f"<@{developer}>" for developer in config["roles"]["developers"]])}
        """

        await ctx.response.send_message(text)

    @app_commands.command(name="rpc", description="Setup your Discord RPC")
    @admin_only()
    async def rpc(self, ctx: discord.Interaction):
        rpc_list = self.bot.config["status"]["loop"]
        text = ""
        for i, rpc in enumerate(rpc_list):
            text += f"{i+1}. {rpc['message']} ({rpc['type']})\n"
        await ctx.response.send_message(text,view=RPCView(self.bot))

    @app_commands.command(name="scripts", description="Your scripts")
    @admin_only()
    async def skript(self, ctx: discord.Interaction):
        await ctx.response.send_message("Your scripts", view=ScriptView(self.bot))

    @app_commands.command(name="compile", description="Compile your scripts")
    @owner_only()
    async def compile(self, ctx: discord.Interaction, script: str):
        await ctx.response.send_message(f"Compiling script: {script}...\n It's better to read output/debug in console.", ephemeral=True)
        if not script.startswith("scripts/"):
            script = f"scripts/{script}"
        if not script.endswith(".tusk"):
            script = f"{script}.tusk"
        try:
            await self.bot.compile_script(script)
            await ctx.followup.send("Scripts compiled!", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"Error compiling script: ```python\n{e}```", ephemeral=True)
    
    @app_commands.command(name="test", description="Test your script")
    @owner_only()
    async def test(self, ctx: discord.Interaction):
        await ctx.response.send_modal(TestModal(self.bot))
    
    @app_commands.command(name="remove_associated_data", description="Remove associated data")
    @owner_only()
    async def remove_associated_data(self, ctx: discord.Interaction, script:str):
        await ctx.response.send_message("Removing associated data...", ephemeral=True)
        self.bot.remove_script_associations(script)
        await ctx.followup.send("Associated data removed!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(TuSKSetup(bot))
from cog_core import *
import discord
import os

global tuskdir
tuskdir = "scripts"
def fm_ui():
    string = f"""```yml
Directory: {tuskdir}

Files:

"""
    
    for file in os.listdir(tuskdir):
        string += f"- {file}\n"
    return string+"\n```"

def delete_file(name:str):
    os.remove(f"{tuskdir}/{name}.tusk")
    return f"Deleted {name}.tusk"

def edit_file(name:str, content:str):
    with open(f"{tuskdir}/{name}", "w") as f:
        f.write(content)
    return f"Edited {name}"

class TestModal(discord.ui.Modal):
    def __init__(self, bot, fake_channel:discord.TextChannel=None, fake_user:discord.Member=None):
        self.bot = bot
        super().__init__(title="Test Script")
        self.fake_channel = fake_channel
        self.fake_user = fake_user
        self.add_item(discord.ui.TextInput(label="Script", style=discord.TextStyle.paragraph, placeholder="print('Hello world!')"))

    async def on_submit(self, interaction: discord.Interaction):
        script = self.children[0].value
        await interaction.response.send_message(f"Compiling Script: {script}", ephemeral=True)
        try:
            await self.bot.compile_script(script, temporary=True,data={
                "fake_channel":self.fake_channel,
                "fake_user":self.fake_user
            })
            await interaction.followup.send("Script compiled!", ephemeral=True)
        except Exception as e:
            print(e.with_traceback())
            await interaction.followup.send(f"Error compiling script: ```python\n{str(e.with_traceback())}```", ephemeral=True)

class ScriptAddForm(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Add a script")
        self.bot = bot
        self.add_item(discord.ui.TextInput(label="Script Title", style=discord.TextStyle.short, placeholder="example.tusk, should end with .tusk or .tuskcmd"))
        self.add_item(discord.ui.TextInput(label="Script", style=discord.TextStyle.paragraph, placeholder="print 'Hello world!'"))

    async def on_submit(self, interaction: discord.Interaction):
        title = self.children[0].value
        script = self.children[1].value

        with open(f"scripts/{title}", "w") as f:
            f.write(script)
        await interaction.response.send_message(f"Script added: {title}\nCompile it with `/compile`", ephemeral=True)
        self.bot.load_scripts()
    
class ScriptRemoveView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
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
        super().__init__()
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
        super().__init__()
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
        filename = os.path.basename(self.value)
        new_path = os.path.join(os.path.dirname(self.value), f"--{filename}")
        os.rename(self.value, new_path)
        self.bot.remove_script_associations(self.value)
        await interaction.response.send_message(f"Script disabled!", ephemeral=True)
        self.bot.load_scripts()



class ScriptView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Add Script", style=discord.ButtonStyle.primary)
    async def add_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_modal(ScriptAddForm(self.bot))

    @discord.ui.button(label="Remove Script", style=discord.ButtonStyle.red)
    async def remove_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Remove Script", view=ScriptRemoveView(self.bot), ephemeral=True)

    @discord.ui.button(label="Enable Script", style=discord.ButtonStyle.green)
    async def enable_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Enable Script", view=EnableScriptView(self.bot), ephemeral=True)

    @discord.ui.button(label="Disable Script", style=discord.ButtonStyle.red)
    async def disable_script(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("Disable Script", view=DisableScriptView(self.bot), ephemeral=True)

class FileManagerGroup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    group = app_commands.Group(name="scripts", description="File Manager (manage scripts)")
    
    @group.command(name="list", description="List all files in the current directory")
    @owner_only()
    async def list_callback(self, ctx: discord.Interaction):
        await ctx.response.send_message(fm_ui())

    @group.command(name="open", description="Open File/Script Manager")
    @owner_only()
    async def open_callback(self, ctx: discord.Interaction):
        # File manager capable of creating, deleting, and editing and compiling tusk files.
        await ctx.response.send_message(fm_ui(),view=ScriptView(self.bot))

    @group.command(name="compile", description="Compile your scripts")
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
    
    @group.command(name="test", description="Test your script")
    @owner_only()
    async def test(self, ctx: discord.Interaction, fake_channel:discord.TextChannel=None,  fake_user:discord.Member=None):
        await ctx.response.send_modal(TestModal(self.bot, fake_channel, fake_user))
    
    @group.command(name="remove_associated_data", description="Remove associated data")
    @owner_only()
    async def remove_associated_data(self, ctx: discord.Interaction, script:str):
        await ctx.response.send_message("Removing associated data...", ephemeral=True)
        # Ensure script has the correct path format
        if not script.startswith("scripts/"):
            script = f"scripts/{script}"
        if not script.endswith(".tusk"):
            script = f"{script}.tusk"
        self.bot.remove_script_associations(script)
        await ctx.followup.send("Associated data removed!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(FileManagerGroup(bot))
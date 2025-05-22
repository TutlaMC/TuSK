# Package Manager for Tusk

from cog_core import *
import requests
import os
import json
# A Package Manager for Tusk
def get_package_sources(bot):
    return bot.config["package_sources"]

package_dir = "packages"

class WimpGroup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    group = app_commands.Group(name="wimp", description="Package Manager for Tusk")


    @group.command(name="list",description="List all packages")
    @owner_only()
    async def list_callback(self, ctx: discord.Interaction,page:int=1):
        ctx.client.reload_config()
        packages = os.listdir(package_dir)
        PackageEmbed = discord.Embed(title="Wimp Package Manager")

        # Page Generator
        pages = []

        c = 0
        cpage = []
        for package in packages:
            c += 1
            if c <= 10:
                cpage.append(package)
            else:
                pages.append(cpage)
                cpage = []
                c = 0
        pages.append(cpage)

        # Add Packages to Embed
        if page > len(pages):
            await ctx.response.send_message(f"Page {page} not found, this either means you don't have package or under rare circumstanes wimp is broken")
            return
        for package in pages[page-1]:
            desc = "No Description"
            if os.path.exists(f"{package_dir}/{package}") and package.endswith(".py"):
                if package != "__init__.py":
                    with open(f"{package_dir}/{package}","r") as f:
                        lines = f.readlines()
                        if lines[0].startswith("#"):
                            desc = lines[0]
                    PackageEmbed.add_field(name=package.capitalize(),value=desc)

        PackageEmbed.set_footer(text=f"Page {page} of {len(pages)}\nYou are using Wimp Package Manager by Tutla Studios")
        await ctx.response.send_message(f"You have {len(packages)} packages installed",embed=PackageEmbed)
  
    @group.command(name="source",description="Add/Remove a package source")
    @owner_only()
    async def source_callback(self, ctx: discord.Interaction, name:str, url:str=None, branch:str="main"):
        ctx.client.reload_config()
        if name in get_package_sources(self.bot):
            with open("config.json","r") as f:
                config = json.load(f)
            config["package_sources"].pop(name)
            with open("config.json","w") as f:
                json.dump(config,f)
            await ctx.response.send_message(f"Removed {name} from package sources")
        else:
            if url is None:
                await ctx.response.send_message(f"Please provide a url for the package source (github only)")
                return
            with open("config.json","r") as f:
                config = json.load(f)
            config["package_sources"][name] = {"url":url,"branch":branch}
            with open("config.json","w") as f:
                json.dump(config,f)
            await ctx.response.send_message(f"Added {name} to package sources")

        ctx.client.reload_config()

    @group.command(name="list_sources",description="List all package sources")
    @owner_only()
    async def list_sources_callback(self, ctx: discord.Interaction):
        ctx.client.reload_config()
        sources = get_package_sources(self.bot)
        await ctx.response.send_message(f"Package sources: {sources}")

    @group.command(name="uninstall",description="Uninstall a package")
    @owner_only()
    async def uninstall_callback(self, ctx: discord.Interaction, package:str):
        ctx.client.reload_config()
        if package+".py" not in os.listdir(package_dir):
            await ctx.response.send_message(f"Package {package} not found")
            return
        os.remove(f"{package_dir}/{package}.py")
        await ctx.response.send_message(f"Uninstalled {package}")

    @group.command(name="install",description="Install a package from source")
    @owner_only()
    async def install_callback(self, ctx: discord.Interaction, package:str, source:str="wimp-official", as_core:bool=False):
        ctx.client.reload_config()
        if source not in get_package_sources(self.bot):
            await ctx.response.send_message(f"Source {source} not found")
            return
        if package+".py" in os.listdir(package_dir):
            await ctx.response.send_message(f"Package {package} already installed")
            return
        
        url = get_package_sources(self.bot)[source]["url"]
        branch = get_package_sources(self.bot)[source]["branch"]
        if "github.com" in url:
            url = url.replace("github.com", "raw.githubusercontent.com")
            url = url.rstrip("/")
            raw_url = f"{url}/{branch}/{package.replace(".","/")}.py"
        else:
            raw_url = f"{url}/{package}.py"

        file = requests.get(raw_url)
        if file.status_code != 200:
            await ctx.response.send_message(f"Package {package} not found")
            return
        with open(f"{package_dir}/{package.split('.')[len(package.split('.'))-1]}.py","w") as f:
            f.write(file.text)
        await ctx.response.send_message(f"Installed {package}!")
            
    @install_callback.autocomplete('source')
    async def source_autocomplete(self, interaction: discord.Interaction, current: str):
        sources = get_package_sources(self.bot)
        packages = []
        for source in sources:
            packages.append(app_commands.Choice(name=source, value=source))
        return packages[:25]
    
    

async def setup(bot: commands.Bot):
    await bot.add_cog(WimpGroup(bot))
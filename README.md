# Discord Bot Shell (CLI)

## Available Commands

### Server Management
- **`servers`**: List all servers the bot is currently in.
- **`connect <guild_id>`**: Connect to a specific server by its name.
- **`channels`**: List all text channels in the connected server.
- **`join <channel_id>`**: Join a channel using its ID.
- **`admins`**: List all admins in the connected server.
- **`members`**: List all members in the connected server.
- **`roles`**: List all roles available in the connected server.

### Message Management
- **`send <message>`**: Send a message to the currently connected channel.
- **`messages <channel_id>`**: Fetch recent messages from a specific channel.
- **`message_count <channel_id>`**: Count the number of messages in a channel.
- **`clear <channel_id> <number_of_messages>`**: Clear recent messages (limit specifies how many to clear).

### User Management
- **`ban <user_id>`**: Ban a user from the connected server by their user ID.
- **`unban <user_id>`**: Unban a user from the connected server by their user ID.

### Bot Information & Actions
- **`info`**: Display information about the bot and the connected server.
- **`ping`**: Check the bot's responsiveness.
- **`invite`**: Generate an invite link for the bot.
- **`quit`**: Exit the CLI and stop the bot.

### Nuking Commands
- **`nuke <args>`**: Execute the 'nuke' command for a specific target (be cautious!).
  
### Help
- **`help`**: Display this help message.

### Install
- To install clone this repository and install all the required packages using `pip install -r requirements.txt`. Then run the code with `python3 app.py`.
## Contributing

Feel free to submit issues, fork the repository, and create pull requests to improve the bot. If you have any suggestions or improvements, please open an issue.

## License

This project is licensed under the MIT License.

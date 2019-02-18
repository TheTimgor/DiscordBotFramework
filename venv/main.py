import asyncio, discord, json, shlex, pydoc

startup = True

with open('config.json', 'r') as read_file:
    global config
    config = json.load(read_file)

client = discord.Client()

# background task
# runs once a second
async def do_in_background():
    while True:
        # put your code here
        await asyncio.sleep(1)

# commands are triggered by a message with the name of the command
# if you're changing/creating a command, remember to update the docstring
class commands:
    @staticmethod
    async def test(params,message):
        """
        awoos
        """
        if params:
            await message.channel.send(params)
        else:
            await message.channel.send('imma wolf awoo')

    @staticmethod
    async def info(params,message):
        """
        info [command]
        """
        if params:
            s = pydoc.getdoc(getattr(commands, params[0]))
            await message.channel.send("Help for {0}:\n```{1}```".format(params[0],s))
        else:
            s = pydoc.getdoc(commands.info)
            await message.channel.send("Help for info:\n```{}```".format(s))

@client.event
async def on_message(message):
    if message.content.startswith(config['trigger']):
        content_str = message.content[len(config['trigger']):]
        content = content_str.split(' ',1)
        command = content[0]
        params = []
        if len(content) > 1:
            params = shlex.split(content[1])
        print(params)
        await getattr(commands, command)(params, message)


@client.event
async def on_ready():
    global startup
    if startup:
        startup = False
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

# uncomment below to run the background task
# client.loop.create_task(do_in_background())
print('running bot')
client.run(config['token'])
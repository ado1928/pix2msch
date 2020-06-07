
# pydustry
A Python package for controlling Mindustry servers and getting their current status

## Documentation:


`pydustry.Server(host, server_port = 6567, socketinput_port = 6859)`

**Server object.**
 - `host` - **String.** Required. IP address of the server
 - `server_port` - **Int.** Defaults at 6567. Port of the server.
 - `socketinput_port` - **Int**. Defaults at 6859. Socketinput port of the server.
#
 `pydustry.Server.get_status()`

Returns the status of the server in the form of a dict.

Example:

 `>>> pydustry.Server("exampleserver.com").get_status() `
	will output

    {"name": "Example Mindustry server",
     "map": "Maze",
     "players": 5, 
     "wave": 10, 
     "version": 89, 
     "vertype": "official"}
     
   
 - `"name"` - **String.** Name of the server.
 - `"map"` - **String.** Map that the server is currently on.
 - `"players"` - **Int.** Number of players online.
 - `"wave"` - **Int**. Wave that the server is currently on.
 - `"version"` - **Int.** Version that the server is on
 - `"vertype"` - **String.** Version type of the server.
#
`pydustry.Server.send_command(command)`
Sends a command through the **socketinput** port of the server.
 - `command` - **String.** Required. Command that gets sent to the server
 #
 `pydustry.Server.get_ping(timeout = 10.0)`
 Returns the **delay** it takes packets to come to the server and back in miliseconds **(ping)**.
- `ping` - **Int.**
- `timeout` - **Numeric**, optional
#
 ## Example codes
 

    import pydustry
    
    # A program that will output the playercount and ping
    
    host = input("Enter the IP address of the Mindustry server:")
    port = input("Enter the port of the Mindustry server:")
    
    server = pydustry.Server(host, int(port))
    
    playercount = server.get_status()["players"]
    ping = server.ping()
    
    print("The number of players is: " + str(playercount))
    print("And the ping is: " + str(ping))
#
    import pydustry, time
    
    # A program that will autosave the local server every 5 minutes
    
    server = pydustry.Server("localhost")
    
    while True:
        server.send_command("save 0")
        server.send_command("say Saved!")
        time.sleep(300)

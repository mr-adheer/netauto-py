"""Step 1: connect to one switch with Netmiko and run one show command."""
# The line above, in triple quotes, is a "docstring": a description of the file.
# Python ignores it when running; it's documentation for humans (and tools).

# ---------------------------------------------------------------------------
# Imports: load the tools this script needs.
# ---------------------------------------------------------------------------

# getpass is built into Python. It asks for input like input() does,
# but doesn't show what you type on the screen, so it suits passwords.
from getpass import getpass

# ConnectHandler is Netmiko's main entry point. You give it the device
# details, and it opens an SSH session and gives you back a connection object.
from netmiko import ConnectHandler

# ---------------------------------------------------------------------------
# Device details, kept in a dictionary (key: value pairs, like YAML).
# ---------------------------------------------------------------------------

switch = {
    # Tells Netmiko which kind of device this is, so it knows the prompts,
    # how to turn off paging ("terminal length 0"), how to enter enable, etc.
    # Similar to ansible_network_os: cisco.ios.ios in Ansible.
    "device_type": "cisco_xe",

    # Management IP of switch.
    "host": "10.10.10.5",

    # input() prints the text, waits for you to type, and returns what you typed.
    "username": input("Username: "),

    # getpass() does the same but hides your typing.
    # The password lives only in memory while the script runs, never in this file.
    "password": getpass("Password: "),
}

# ---------------------------------------------------------------------------
# Connect, run commands, disconnect.
# ---------------------------------------------------------------------------

# ConnectHandler(**switch) opens the SSH session.
#   **switch unpacks the dictionary into named arguments, the same as writing:
#   ConnectHandler(device_type="cisco_xe", host="10.10.10.5", username=..., password=...)
#
# "with ... as conn:" is a context manager:
#   - the session is opened and stored in the variable "conn"
#   - the indented block below runs
#   - when the block ends (normally or because of an error), the session is closed
# Without "with", you would have to remember to call conn.disconnect() yourself.
with ConnectHandler(**switch) as conn:

    # Ask the switch for its current prompt, e.g. "blr-flr1-acc-sw01#".
    # A "#" means privileged EXEC; ">" means user EXEC, where some show
    # commands fail. We only look at it for now; handling ">" comes later.
    prompt = conn.find_prompt()

    # Send one show command and wait for the full answer.
    # Netmiko waits until the prompt comes back, then returns all the text
    # in between as one string, stored in "output".
    # output = conn.send_command("show ip int brief")
    output = conn.send_command("show ip int brief")

# The session is closed at this point; we only work with the saved text now.

# ---------------------------------------------------------------------------
# Show the results.
# ---------------------------------------------------------------------------

# f-string: the f before the quotes lets you place variables inside {}.
# Like "{{ prompt }}" in a Jinja template.
print(f"Landed at prompt: {prompt}")

# Print the full show version output exactly as the switch sent it.
print(output)

# Cut the text into a list, one item per line
lines = output.splitlines()

# len() counts items in the list, so this is the number of lines
print(f"Output has {len(lines)} lines")

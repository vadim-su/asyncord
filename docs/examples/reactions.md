The reactions example is a simple bot. It will respond to the following command on discord:
```plaintext
/reactions
```
It outputs a panel with 3 buttons. Clicking on the buttons will make bot react to the message.

::: examples.reactions_bot.main

Not all behavior can be achievied as a response to event. 
This example makes use of separate http_client calls to add/remove reactions. 

Note that the application still needs to answer the interaction within 3 seconds.
This example makes use of ephemerial(visible only to the user) messages as a response to the interactions.

*Pong response to an interaction is not meant for such purposes and doesn't work this way. Ephemerial messages are the best practice here. 

::: examples.reactions_bot.commands


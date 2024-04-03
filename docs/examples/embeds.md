The embed example is a simple weather bot. It will respond to the following command on discord:
```plaintext
/weather 'city'
```
It fetches the weather data from 3rd party API with a passed city as an argument.


::: examples.weather_embed.main

The ChatCommand ABC class represents a command pattern. 
It has a register method, which adds event handlers to the Event Dispatcher. 
And the command method as a handler.

You can inherit from the ChatCommand class and implement the command method to create a new command.

Interactions should be answered by the bot within 3 seconds, unless detered. 



::: examples.weather_embed.commands

## Models for 3rd party API in this example

::: examples.weather_embed.models
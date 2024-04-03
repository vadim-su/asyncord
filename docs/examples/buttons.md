The button example is a simple poll bot. It will respond to the following command on discord:
```plaintext
/poll
```
Creating a simple poll with 3 questions and 3 options each. 

Upon the answer of the user, the bot will save the answer and edit the message with a next question.
When all questions are answered, the bot will output the answers. 



The example is primitive and compomises the answer storage and is meant to be a simple example of how to use buttons.

::: examples.trivia_bot.main

The PollCommand represents a command pattern. 
It has a register method, which adds event handlers to the Event Dispatcher. 
And the handlers for the events. 

The handlers take interaction events as an arguments, which are passed by the event dispatcher when the event is registered.
The interaction events are created by the discord and sent over Gateway when a user interacts with a message.
In this example they represent the button clicks and command call.  

Interactions should be answered by the bot within 3 seconds, unless detered. 

Use custom_id to identify the button.


::: examples.trivia_bot.commands
# Client Hub

The `ClientHub` is a class that manages the connection to the Discord API. 
Under the hood it creates instances of the Gateway and HTTP clients under one `ClientGroup`. 
The `ClientHub` can hold multiple `ClientGroup` instances, each with their own Gateway and HTTP clients,
allowing you to connect to multiple Discord bots at the same time.

You can omit the usage of the `ClientHub` and use the `Gateway` and `HTTP` clients directly. 
For example, if you only need one of those two. 

::: asyncord.client_hub
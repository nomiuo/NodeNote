# Plugin
NodeNote supports hot plugin.

Manager will load, registry, unload plugin.
The api version invoked by plugin must be provided.
Meta data file or Internal code.
Plugins run in a seprate progress and communicate with the core api through IPC channel.
Load plugins by different symbols.

## Core api
init
free
registry

# Custom Widgets
## package.component.base_component.BaseComponent class

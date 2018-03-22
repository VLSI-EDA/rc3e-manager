# Read Me

This is a project of the chair for VLSI design and architecture
at the faculty of Computer Science
of the Technische Universität Dresden, Germany.

It is free for public use.

## General Design Principles

All operations on objects represented by database entries fall in one
of the following categories:

* **Create** instantiates a new object.
Additionally, helper objects may be created alongside it as well.
* **Delete** removes an object and its associated helper object.
A deletion may cause further cascading deletions.
* **List** presents all objects of a given type.
Details of the objects may be omitted.
* **Show** displays details about an object and helper objects.

Each of these interactions may be restricted by user permissions.

## Interfaces

Two interfaces are offered by the system:
* A **Web API** intended for human interaction
* A **REST API** intended for machine interaction

Which interface is used, gets determined by the URL
to which the browser/client sends an _HTTP_ request is sent.

Both interfaces act on the same model and database backend.
If the URL `<hostname>:<port>/` is used without any following API
specification, a welcome page leading to the _Web API_ will be
returned.

### The Web API

The _Web API_ can be reached using the URL
```
<hostname>:<port>/web_api/<resource>/<action>
```

* **Resource** is the plural name of the object to interact with
* **Action** is the action to do on this object. This might be followed
by URL parameters to specify the object on which to perform the action
if the action requires it.

Examples:
```
# Lists all FPGAs
localhost:8000/web_api/fpgas/list

# Shows details on FPGA with ID 2
localhost:8000/web_api/fpgas/show/2/
```


All requests to this API must be _HTTP_ _POST_ requests.

### The REST API
The _REST API_ can be reached using the URL `<hostname>:<port>/rest_api/`.
# Readme

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
The list may be restricted by user permissions.
Not all details of objects may be shown.
* **Show** displays details about an object and helper objects.
This view may be restricted by user permissions.
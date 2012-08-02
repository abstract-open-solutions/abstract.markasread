=====================
Abstract Mark as Read
=====================

Introduction
============

This package defines new functionality for Plone Objects (Page, Event, New Item, etc.).

This feature allows authenticated users to mark as 'read' documents objects.

Manager can choose which content types apply new functionality to.

How it works
============

Authenticated user can marks as read any "markable" object.

Manager can choose wich types apply functionality to.

By default only Event and Page types are extended.

New viewlet is added for "mark as read" feature below content.


How to use
==========

This package provides a configlet that makes possibile to choose the set
of portal-types which to attach the new feature (roo-url/@@markasread-controlpanel).

Also you (Manager) can insert text to show into viewlets.

This settings are stored into portal_registry.

When an authenticated user is on some object (one of the types listed in configlet),
custom viewlet id rendered below content body.

In this viewlet is shown selected text and form to submit "mark as read".

Current object is annotated (via custom adapter) and the username of current authenticated 
user is stored into object's annotation.


Dependencies
============

* Plone 4.2.x


License
=======
GNU GPL v2 (see docs/LICENCE.txt for details)

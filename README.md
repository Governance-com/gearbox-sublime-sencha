#Gearbox Sublime Sencha
Congratulations! You're about to supercharge your Ext JS development.
The Gearbox Sublime Sencha plugin aids development with snippets, shortcuts and
a little bit of magic.

[TOC]

##Prerequisites
In order to use this package to its full extent, you should first install:

- [Sencha CMD](http://docs.sencha.com/cmd/index.html)
- [JsDuck](https://github.com/senchalabs/jsduck)
- [Sublime Text](https://www.sublimetext.com)

##Installation
The only installation steps to take after installing this sublime package are [configuring](#configuration) the package and tell JsDuck to build the docs for the first time. Once configured, run the Rebuild jsDuck [command](#commands) form a file in your project and you're all set!

##Related Files
The related files plugin helps you quickly switch between files that are strongly related, like the Model, View and Controller of the same type.

## Snippets
Snippets speed up your development by shortening the code you write over and over again. Like a class definition. The Gearbox Sublime Sencha Gear offers four kinds of snippets: 

- [Ext JS specific snippets](#ext-js-specific-snippets)
- [Definition snippets](#definition-snippets)
- [Convenience snippets](#convenience-snippets)
- [Testing snippets](#testing-snippets)

###Ext JS specific snippets
afterRender
:	*tabTrigger*: afterRender
	*selection*: Added as the function body
Adds an afterRender method to your class, with a call to the parent.

callParent
:	*tabTrigger*: callParent
	Adds a call to the parent with arguments.

constructor
:	*tabTrigger*: constructor
Adds a constructor with ApplyIf and a call to the parent.

create
:	*tabTrigger*: create
	*after*: Ext.Component, config
	Creates an Ext.create statement.

define
:	*tabTrigger*: define
	*after*: name, parent, xtype, body
	*selection*: Added as body
	Creates an Ext.define statement

requires
:	*tabTrigger*: requires
	Adds an empty requires array.

initComponent
:	*tabTrigger*: initComponent
	Inserts Ext JS' initComponent function, with a call to the parent.

items
:	*tabTrigger*: items
	Inserts an array of objects.

mixins
:	*tabTrigger*: mixins
	Adds a mixins block with some default Gearbox mixins.

###Definition snippets
f
:	*tabTrigger*: f	
	Adds a new anonymous function

fn
:	*tabTrigger*: fn	
	Inserts a new anonymous method
	
function
:	*tabTrigger*: function
	Adds a new anonymous function with a debug line.

###Gearbox snippets
log
:	*tabTrigger*: log
	*selection*: As argument to the logger. 
	Adds a call to a local logger: this.log

log variable
:	*tabTrigger*: logv
	Add a log showing the value of a variable.
	
log annotated
:	*tabTrigger*: loga
	Same as logv, but with an annotation.

###Convenience snippets
console.log variable
: 	*tabTrigger*: clogv
	Add a console.log statement to output a variable and its value.

debug
:	*tabTrigger*: debug
	*after*: The object to debug
	Adds a call to this.debug with arguments as the default argument.

each
:	*tabTrigger*: each
	Adds a lodash each block. 
	
eachPush
:	*tabTrigger*: eachPush
	Same as each, but push each item to an array. 
	
line
:	*tabTrigger*: line
	Adds a line of dashes.

map
:	*tabTrigger*: map
	Adds a lodash map block. 

next
:	*tabTrigger*: next
	Create a new function with a next function as argument.

promise
:	*tabTrigger*: promise
	Add a return Promise block

###Testing snippets
describe
:	*tabTrigger*: describe
	Insert t.describe block. 
	
it
:	*tabTrigger*: it	
	Insert t.it block.

requireOK
:	*tabTrigger*: requireOK
	Insert a requireOK block.

startTest
:	*tabTrigger*: startTest
	 Insert a startTest block.

##Commands
The listed keycodes are the defaults. You can change them in the [configuration](#configuration).

Related Files
:	*command*: related_files
	*shortcut*: alt+shift+p

Related Files Lucky
:	*command*: related_files_lucky
	*shortcut*: ctrl+shift+alt+p

Class functions
:	*command*: class_functions
	*shortcut*: super+alt+r

Class properties
:	*command*: class_properties
	*shortcut*: super+alt+ctrl+r

Class related classes
:	*command*: class_related_classes
	*shortcut*: super+alt+p

Restart Sublime (dev only)
:	*command*: restart_sublime
	*shortcut*: f5

Rebuild jsDuck
:	*command*: rebuild_jsduck


##Configuration

###Advanced
These settings are only for advanced users. For a normal project, you won't need to edit any of this.

####Related Files
In the relatedFiles.sublime-settings file, you can tell the package where to look for related files. This is done using a regexes, but don't despair; the next paragraphs will help you configure it even if you've never written a single regex in your life. 

#####Where to look in general
The file contains a big commented regex and a couple of smaller regexes, the big one tells the plugin where to look for your js files, the smaller ones tell it where to look for related files.

Here's the big one:

	^.+?\/(?:app|src|tests)(?:\/\\w*)?(?:\/fund)?\/?(.*\/?)?\/(\\w*)(?:\\.t)?\\.js$

Scary, huh? Fear not, for a normal project, you'll need not edit anything. This regex describes the general structure of your project. 

#####Where to look for related files.

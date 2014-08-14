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

All configuration options explained.

### "propertyTemplates"
Snippet templates used to insert properties into the file **< name >** gets replaced with the property name.
This format uses 1 array entry per line, and supports Sublime Snippet features.

	"String": [
		"<name>: '$1'"
	],
	"Boolean": [
		"<name>: ${1:false}"
	],
	"Object": [
		"<name>: {",
		"	'$1': '$1'",
		"}"
	],
	"Array": [
		"<name>: [",
		"	${1:''}",
		"]"
	],
	"Number": [
		"<name>: ${1:0}"
	]

### "functionTemplate"
Snippet templates used to insert functions into the file **< name >** gets replaced with the property name.
This format uses 1 array entry per line, and supports Sublime Snippet features.

	"<name>: function(config) {",
		"	this.callParent(arguments);",
		"	$1",
	"}"
	
###Advanced
These settings are only for advanced users. For a normal project, you won't need to edit any of this.

#### "autoUpdate"
This is an **experimental** feature still being worked on, it will try to update class information in the background.

	"enabled": false,
	"interval": 300



#### "applicationPaths"
Paths the plugin will look for a valid application folder, relative to working directory root.

	[
		"/desktop",
		"/"
	]

#### "jsduckduckPaths"
Paths where the plugin will look for valid jsduck formatted data to use to provide related functions/properties/classes, relative to application folder.

	[
		"jsduck",
		"docs"
	]

#### "jsduckduckbuildpaths"
Folders to include when building jsduck information, relative to application folder.

	[
		"app",
		"ext/src"
	]

#### "jsduckduckargs"
Only edit when you really know how jsduck and this plugin works.

####"relatedFilesPatterns"
This is done using a regexes, but don't despair; you don't need to configure anything.

#####Where to look in general
The file contains a big commented regex and a couple of smaller regexes, the big one tells the plugin where to look for your js files, the smaller ones tell it where to look for related files.

Here's the big one:

	^.+?\/(?:app|src|tests)(?:\/\\w*)?(.*\/?)?\/(\\w*)(?:\\.t)?\\.js$

Scary, huh? Fear not, for a normal project, you'll need not edit anything. This regex describes the general structure of your project. 

#####Where to look for related files.

Search for any files matching the following structure($1=currentModuleName, $2=currentFileName):

      "*/model/$2.js",
      "*/model/*/$2.js",
      "*/model/*/*/$2.js",

      "*/$1/$2.*js",
      "*/*/$1/$2.*js",
      "*/*/*/$1/$2.*js",

      "*/packages/gearbox/*/$1/$2.*js",
      "*/packages/gearbox/*/*/$1/$2.*js",

      "*/ext/src/$1/$2.js"
#Gearbox Sublime Sencha
Congratulations! You're about to supercharge your Ext JS development.
The Gearbox Sublime Sencha plugin aids development with snippets, shortcuts and
a little bit of magic.

*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Related Files](#related-files)
*   [Commands](#commands)
*   [Snippets](#snippets)
	*   [Ext JS specific snippets](#ext-js-specific-snippets)
	*   [Gearbox snippets](#gearbox-snippets)
	*   [Convenience snippets](#convenience-snippets)
	*   [Testing snippets](#testing-snippets)
*   [Configuration](#configuration)
	*   [Property Templates](#property-templates)
	*   [Function Template](#function-template)
	*   [Advanced](#advanced)
		*   [Auto Update](#autoupdate)
		*   [application Paths](#application-paths)
		*   [jsduck Paths](#jsduck-paths)
		*   [jsduck buildpaths](#jsduck-buildpaths)
		*   [jsduck args](#jsduck-args)
		*   [Related Files Patterns](#related-files-patterns)
			*   [Where to look in general](#where-to-look-in-general)
			*   [Where to look for related files.](#where-to-look-for-related-files)

##Prerequisites
In order to use this package to its full extent, you should first install:

- [ruby 2.0+](https://www.ruby-lang.org/en/downloads/)
- [Sencha CMD](http://docs.sencha.com/cmd/index.html)
- [JsDuck](https://github.com/senchalabs/jsduck)
- [Sublime Text](https://www.sublimetext.com)

##Installation
The easiest way to install this package is through [sublime package control](https://sublime.wbond.net/), we reccommend you [install](https://sublime.wbond.net/installation) it, if you don't already have it. Then from your Sublime Text editor, open the command prompt (default: Ctrl + ⇧ + P or ⌘ + ⇧ + P) and type "package control install package". Press enter to start the package control (may take a couple of seconds to load), then search for "GearboxSencha".

The only installation steps to take after installing this sublime package are [configuring](#configuration) the package and tell JsDuck to build the docs for the first time. Once configured, run the Rebuild jsDuck [command](#commands) from a file in your project and you're all set!

##Related Files
The related files plugin helps you quickly switch between files that are strongly related, like the Model, View and Controller of the same type.

##Commands
The listed keycodes are the defaults. You can change them in the [configuration](#configuration).

**Related Files**
> 
**command**: related_files		<br/>
**Linux shortcut**: alt+shift+p		<br/>
**Mac OSX shortcut**: alt+shift+p		<br/>

**Related Files Lucky**
> 
**command**: related_files_lucky		<br/>
**Linux shortcut**: ctrl+shift+alt+p		<br/>
**Mac OSX shortcut**: ctrl+shift+⌘+p		<br/>

**Class related classes**
> 
**command**: class_related_classes		<br/>
**Linux shortcut**: super+alt+p		<br/>
**Mac OSX shortcut**: ⌘+alt+p		<br/>

----------

**Class functions**
> 
**command**: class_functions		<br/>
**Linux shortcut**: super+alt+r		<br/>
**Mac OSX shortcut**: ⌘+alt+r		<br/>

**Class properties**
> 
**command**: class_properties		<br/>
**Linux shortcut**: super+alt+ctrl+r		<br/>
**Mac OSX shortcut**:  ⌘+alt+y		<br/>

**Restart Sublime (dev only)**
> 
**command**: restart_sublime		<br/>
**Linux shortcut**: f5		<br/>
**Mac OSX shortcut**: f5		<br/>

**Rebuild jsDuck**
> 
**command**: rebuild_jsduck		<br/>
**Linux shortcut**: super+alt+j		<br/>
**Mac OSX shortcut**: ⌘+alt+j		<br/>

## Snippets
Snippets speed up your development by shortening the code you write over and over again. Like a class definition. The Gearbox Sublime Sencha Gear offers four kinds of snippets: 

- [Ext JS specific snippets](#ext-js-specific-snippets)
- [Definition snippets](#definition-snippets)
- [Convenience snippets](#convenience-snippets)
- [Testing snippets](#testing-snippets)

###Ext JS specific snippets

**afterRender**
> 
**tabTrigger**: afterRender		<br/>
**selection**:	Added as the function body		<br/>
Adds an afterRender method to your class, with a call to the parent.

```javascript
afterRender: function() {
	this.debug(arguments);
	
	this.callParent(arguments);
},
```

**callParent**
> 
**tabTrigger**: callParent		<br/>
Adds a call to the parent with arguments.

```javascript
return this.callParent(arguments);
```

**constructor**
> 
**tabTrigger**: constructor		<br/>
Adds a constructor with ApplyIf and a call to the parent.

```javascript
constructor: function(config) {
	this.debug(arguments);

	Ext.applyIf(config || {}, {
		
	});

	return this.callParent(arguments);
},
```

**create**
> 
**tabTrigger**: create		<br/>
**after**:		Ext.Component, config		<br/>
Creates an Ext.create statement.

```javascript
Ext.create('', {
	
});
```


**define**
> 
**tabTrigger**: define		<br/>
**after**:		name, parent, xtype, body		<br/>
**selection**:	Added as body		<br/>
Creates an Ext.define statement.

```javascript
Ext.define('', {
	extend: 'Ext.',
	xtype: '',

	//

	mixins: [
		'Gearbox.mixin.ModelInfo',
		'Gearbox.mixin.Logger'
	],

	logLevel: 'debug',

	//

	
});e
```


**requires**
> 
**tabTrigger**: requires		<br/>
Adds an empty requires array.

```javascript
requires: [
	''
],
```


**initComponent**
> 
**tabTrigger**: initComponent		<br/>
Inserts Ext JS' initComponent function, with a call to the parent.

```javascript
initComponent: function() {
	this.debug(arguments);
	
	this.callParent(arguments);
},
```


**items**
> 
**tabTrigger**: items		<br/>
Inserts an array of objects.

```javascript
items: [{
	
}],
```


**mixins**
> 
**tabTrigger**: mixins		<br/>
Adds a mixins block with some default Gearbox mixins.

```javascript
mixins: [
	'Gearbox.mixin.ModelInfo',
	'Gearbox.mixin.Logger'
],

logLevel: 'debug',

//
```


**###Definition snippets**
> 
**tabTrigger**: f			<br/>
Adds a new anonymous function.

```javascript
function() {
	
}
```


**fn**
> 
**tabTrigger**: fn			<br/>
Inserts a new anonymous method.

```javascript
: function() {
	this.debug(arguments);

	
},
```


**function**
> 
**tabTrigger**: function		<br/>
Adds a new anonymous function with a debug line.

```javascript
function() {
	this.debug(arguments);

	
},
```


###Gearbox snippets
**log**
> 
**tabTrigger**: log		<br/>
**selection**:	As argument to the logger. 		<br/>
Adds a call to a local logger: this.log.

```javascript
this.log(arguments);
```


**log variable**
> 
**tabTrigger**: logv		<br/>
Add a log showing the value of a variable.

```javascript
this.log('', '=', );
```


**log annotated**
> 
**tabTrigger**: loga		<br/>
Same as logv, but with an annotation.

```javascript
this.log(':', ' =', );
```


###Convenience snippets
console.log variable
: 	*tabTrigger*: clogv		<br/>
Add a console.log statement to output a variable and its value.

```javascript
console.log('', '=', );
```


**debug**
> 
**tabTrigger**: debug		<br/>
**after**:		The object to debug		<br/>
Adds a call to this.debug with arguments as the default argument.

```javascript
this.debug(arguments);
```


**each**
> 
**tabTrigger**: each		<br/>
Adds a lodash each block. 

```javascript
_.each(arr, function(item, key) {
	console.log('item:', key, '=', item);
	
});
```


**eachPush**
> 
**tabTrigger**: eachPush		<br/>
Same as each, but push each item to an array. 

```javascript
var items = [];
_.each(arr, function(item, key) {
	console.log('arr:', key, '=', item);
	
	items.push(item);
});
```


**line**
> 
**tabTrigger**: dashes		<br/>
Adds a line of dashes.

```javascript
////////////////////////////////////////////////////////////////////////////
```


**map**
> 
**tabTrigger**: map		<br/>
Adds a lodash map block. 

```javascript
var items = _.map(arr, function(item, key) {
	this.log('arr:', key, '=', item);

	return item;
}, this);
```


**next**
> *tabTrigger*: next		<br/>
Create a new function with a next function as argument.

```javascript
function(next) {
	
	next();
}
```


**promise**
> 
**tabTrigger**: Promise		<br/>
Add a return Promise block.

```javascript
return new Promise(function(resolve, reject) {
	
});
```


###Testing snippets
**describe**
> 
**tabTrigger**: describe		<br/>
Insert t.describe block. 

```javascript
t.describe('', function(t) {
	
});
```


**it**
> 
**tabTrigger**: it			<br/>
Insert t.it block.

```javascript
t.it('should ', function(t) {
	
});
```


**requireOK**
> 
**tabTrigger**: requireOK		<br/>
Insert a requireOK block.

```javascript
t.requireOk([
	''
]);
```


**startTest**
> 
**tabTrigger**: startTest		<br/>
Insert a startTest block.

```javascript
startTest(function(t) {
	
});
```


##Configuration

All configuration options explained.

### propertyTemplates
Snippet templates used to insert properties into the file **< name >** gets replaced with the property name.
This format uses 1 array entry per line, and supports Sublime Snippet features.

```json
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
```

### "functionTemplate"
Snippet templates used to insert functions into the file **< name >** gets replaced with the property name.
This format uses 1 array entry per line, and supports Sublime Snippet features.

```json
"<name>: function(config) {",
	"	this.callParent(arguments);",
	"	$1",
"}"
```

###Advanced
These settings are only for advanced users. For a normal project, you won't need to edit any of this.

#### "autoUpdate"
This is an **experimental** feature still being worked on, it will try to update class information in the background.

```json
"enabled": false,
"interval": 300
```

#### "applicationPaths"
Paths the plugin will look for a valid application folder, relative to working directory root.

```json
[
	"/desktop",
	"/"
]
```

#### "jsduckPaths"
Paths where the plugin will look for valid jsduck formatted data to use to provide related functions/properties/classes, relative to application folder.

```json
[
	"jsduck",
	"docs"
]
```

#### "jsduckbuildpaths"
Folders to include when building jsduck information, relative to application folder.

```json
[
	"app",
	"ext/src"
]
```

#### jsduckargs
Only edit when you really know how jsduck and this plugin works.

####relatedFilesPatterns
This is done using a regexes, but don't despair; you don't need to configure anything.

#####Where to look in general
The file contains a big commented regex and a couple of smaller regexes, the big one tells the plugin where to look for your js files, the smaller ones tell it where to look for related files.

Here's the big one:

```javascript
^.+?\/(?:app|src|tests)(?:\/\\w*)?(.*\/?)?\/(\\w*)(?:\\.t)?\\.js$
```

Scary, huh? Fear not, for a normal project, you'll need not edit anything. This regex describes the general structure of your project. 

#####Where to look for related files.
Search for any files matching the following structure($1=currentModuleName, $2=currentFileName):

```javascript
"*/model/$2.js",
"*/model/*/$2.js",
"*/model/*/*/$2.js",

"*/$1/$2.*js",
"*/*/$1/$2.*js",
"*/*/*/$1/$2.*js",

"*/packages/gearbox/*/$1/$2.*js",
"*/packages/gearbox/*/*/$1/$2.*js",

"*/ext/src/$1/$2.js"
```

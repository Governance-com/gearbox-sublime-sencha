# Sublime Text 3 - Gearbox Plugin

.. TODO add gearbox description

![Screenshot](https://raw.github.com/fabiokr/sublime-related-files/master/screenshots/list.png)

This plugin provides a quick list of related files to the currently open file.

My main use case is to list related files under a Ruby on Rails project. For example, for an opened "app/controllers/examples_controller.rb", related files would be "app/helpers/examples_helper.rb", "app/views/examples/**", and "spec/controllers/examples_controller_spec.rb".

This plugin was inspired by the existing [Open Related](https://github.com/vojtajina/sublime-OpenRelated) and [Rails Related Files](https://github.com/luqman/SublimeText2RailsRelatedFiles).

I wanted something between the two of them (a quick list of results that could be setup for any kinds of projects, not only Rails), so I created my own.

# Key Shortcut

The default shortcut is mapped to "ctrl+super+p". To change it to something more suitable for your needs, you can easily change that by copying the following and replacing the "keys" to your desired key combination:

```json
{ "keys": ["ctrl+super+p"], "command": "related_files"}
```

# Configuration

The plugins comes configured to lookup Rails related files, but you can add your own setups. Let's see an existing example:

```json
// Test/specs for ruby files
".+\/(app|lib)\/(.+).rb":
  [
    "spec/$2_spec.rb",
    "test/$2_test.rb"
  ]
```

The configuration has two parts: the key, which is a regular expression to match against the currently open file, and a list of globs to map the related files.

You can use the $1, $2, etc. on the glob strings to be replace by the extracted parts from the regex.

In addition to global configs, you can also have per project configs. To add that, in a sublime project file (project-name.sublime-project),
add this:


```json
{
  "settings":
  {
    "RelatedFiles": {
      "patterns": {
        // you project patterns
      }
    }
  }
}
```

Python EmberBuild
=======================

A skeleton application framework using Ember.js, minispade and EmberBuild.

Inspiration from https://github.com/interline/ember-skeleton/, the purpose of building this was to eliminate a heavy set of dependancies and remove 
boiler-plate loader files like controllers.js, view.js etc.

EmberBuild will simply keep a list of all controllers, models and views and include them directly in the 'main' module.


Running
-------
    $ ember_build.py /path/to/project

    You can also use this as a library in your own project just include ember.py. (see ember_build for usage)


Commandline flags
-------
    usage: ember_build.py [-h] [-t dev] [-v] project

    positional arguments:
        project             Path to Ember project you want to compile

    optional arguments:
        -h, --help          show this help message and exit
        -t dev, --type dev  Change Ember build type (live or dev)
        -v                  Change output verbosity (0-2) defaults to 0

    In your browser visit index.html after you've ran the build process.



App Structure
-------------
where (m) is not specified all files will be kept as is.
(m) indicates that the file is modularized during building.

    ember-skeleton
    ├── app - App specific code
    │   ├── .compiled - Build out directory
    │   │   └──app.js - Built out app JS
    │   │   └──minispade.js - JS module loader
    │   ├── controller - 3rd party libraries. (m)
    │   ├── libs - 3rd party libraries. (m)
    │   ├── models - Ember models. (m)
    │   ├── templates - Handlebars templates, (m)
    │   ├── views - Ember views. (m)
    ├── core.js - Boostrap for your Ember app. (m)
    ├── index.html - Boostrap for your Ember app. (m)
    └── router.js - Ember routes. (m)



Todo
-------------
* Add minification when build_type is not dev
* Re-build when any file has changed (inotify)

Python EmberBuild
=======================

A skeleton application framework using Ember.js, minispade and EmberBuild.

Inspiration from https://github.com/interline/ember-skeleton/, the purpose of building this was to eliminate a heavy set of dependancies and remove 
boiler-plate loader files like controllers.js, view.js etc.

EmberBuild will simply keep a list of all controllers, models and views and include them directly in the 'main' module.


Running
-------
    please see sample.py
    $ python sample.py

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

Thanks
------------
You all know who you are. I will update this at some stage *hugs*


Todo
-------------
* Add minification when build_type is not dev
* Re-build when any file has changed (inotify)

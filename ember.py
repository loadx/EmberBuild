import glob
import json
import logging
import os
import time
from shutil import copyfile

logging.basicConfig(level=0, format='[%(levelname)s] %(message)s')

def human_readable_size(size):
    suffixes = [("B", 2 ** 10), ("K", 2 ** 20), ("M", 2 ** 30), ("G", 2 ** 40), ("T", 2 ** 50)]
    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            return round(size / float(lim / 2 ** 10), 2).__str__() + suf


class EmberBuild():
    LIBS_PATH = 'libs'
    TEMPLATES_PATH = 'templates'
    COMPILE_PATH = '.compiled'
    COMPILE_FILENAME = 'app.js'

    def __init__(self, app_path, build_type='dev'):
        self.app_path = os.path.join(os.path.dirname(__file__), app_path)
        self.production_build = False
        self.boostrap_files = []
        self.build_file = os.path.join(self.app_path, self.COMPILE_PATH, self.COMPILE_FILENAME)

        if build_type != 'dev':
            # flag to enable/disable minification and gzip
            self.production_build = True
        try:
            self.build_file = open(self.build_file, 'w+')
        except IOError:
            logging.error('Could not create %s build file', self.build_file)
            return

    def timed(method):
        def timed(*args, **kw):
            """
            Calculate how long the function takes
            """
            ts = time.time() * 1000
            result = method(*args, **kw)
            te = time.time() * 1000

            if method.__name__ == 'generate_bootstrap':
                args[0].curr_file = 'boostrap'

            logging.debug('Built %r in %2.2f milliseconds' % (args[0].curr_file, te - ts))
            return result

        return timed

    def build_libs(self):
        """
        use minispade to compile all files in LIBS_PATH
        """
        # no need for minispade itself to be included
        all_libs = [x for x in glob.glob(os.path.join(self.app_path, self.LIBS_PATH, '*.js')) if 'minispade.js' not in x]
        return self.build_dir(all_libs, 'libs')

    def build_templates(self):
        """
        use minispade to compile all templates to handlebars
        """
        return self.build_dir(os.path.join(self.app_path, self.TEMPLATES_PATH, '*.handlebars'), 'templates')

    def build_app_base(self):
        """
        use minispade to compile all controllers, models and views
        includes router and boostrap core files
        """
        ordered_libs = ['*.js', 'models', 'controllers', 'views']
        for item in ordered_libs:
            path = os.path.join(self.app_path, item)

            if item == '*.js':
                # jump back a folder
                path = os.path.abspath(os.path.join(path, '../../', item))
                self.build_dir(path, '')
            else:
                path += '/*.js'
                self.build_dir(path, item)

    def build_app(self):
        """
        compile all separate javascript files into one large build file
        """
        self.build_templates()
        self.build_libs()
        self.build_app_base()

        # copy minispade to compiled folder
        try:
            minispade_folder = os.path.join(self.app_path, self.LIBS_PATH)
            compiled_folder = os.path.join(self.app_path, self.COMPILE_PATH)
            copyfile(os.path.join(minispade_folder, 'minispade.js'), os.path.join(compiled_folder, 'minispade.js'))
        except IOError:
            logging.error('unable to copy minispade.js from %s to %s' % (minispade_folder, compiled_folder))
            # halt the build process
            return False

        # finishing touch generate the bootstrap file
        self.generate_bootstrap()
        logging.warning('App %r compiled with size of %s' % (self.app_path, human_readable_size(float(self.build_file.tell()))))
        self.build_file.close()

    def build_dir(self, folder_path, type):
        """
        Loop through a directory of files creating
        minispade dependancy libs
        """
        if '*' in folder_path:
            files = glob.glob(folder_path)
        else:
            # this is not a glob use each list item as is
            files = folder_path

        for file in files:
            logging.info("Building %r" % file)
            self.curr_file = file

            try:
                self.build_file.writelines(self.build_minispade_file(file, type))
                self.build_file.writelines("\n")
            except (IOError, AttributeError):
                logging.error('Failed when writing compiled %s to %s' % (file, self.build_file))

    @timed
    def build_minispade_file(self, file, require_path):
        """
        Create the minispade wrapper for 'file'

        output is:
        minispade.register('<name of file>', function(){
            //contents of file
        });

        if the file is of 'type' template then stringify the contents
        and wrap it with Handlebars
        """
        require_name = os.path.join(require_path, os.path.basename(file).replace('.js', ''))
        file_contents = []
        file_buff = open(file)
        prepend_string = ''
        delimeter = '\n'

        for line in file_buff:
            if require_path == 'templates':
                template_name = os.path.basename(file).replace('.handlebars', '')
                require_name = os.path.join(require_path, template_name)

                # escape HTML to be a valid string and wrap in handlebars
                # use concatentation formatting for templates
                prepend_string = '  Ember.TEMPLATES["%s"] = Ember.Handlebars.compile(\n' % template_name
                file_contents.append('      ' + json.dumps(line.rstrip()))
                delimeter = ' +\n'
            else:
                file_contents.append('      ' + line.rstrip())

        string = "minispade.register('%s', function(){\n"
        string += "%s%s\n"
        if require_path == 'templates':
            string += "  );\n"
        string += "});\n"

        # cache out all controllers, models and views
        # we need these to populate the boostrap requires
        if require_path != 'templates' and require_path != 'libs':
            self.boostrap_files.append(require_name)

        file_buff.close()
        return (string) % (require_name, prepend_string, delimeter.join(file_contents))

    @timed
    def generate_bootstrap(self):
        """
        Creates the entry point for the Ember application.
        loads in all controllers, models and views
        """
        string = "minispade.register('main', function(){\n"

        for file in self.boostrap_files:
            logging.info('Adding %r to boostrap' % file)
            string += "    minispade.require('%s');\n" % file

        string += "\n"
        string += "    App.initialize();\n"
        string += "});"

        try:
            self.build_file.writelines(string)
        except (AttributeError, IOError):
            logging.error('Failed when writing compiled boostrap to %s' % self.build_file)

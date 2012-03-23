# build file

from tic.development import closure
import os
import shutil
import logging
from tic import loader2
import re
import errno
import yaml

class BuildCommand(object):
    def __init__(self, **kwargs):
        subparsers = kwargs.get('subparsers')
        self.config = kwargs.get('config')
        
        self.parser = subparsers.add_parser('build',
                                            help='Builds the Google AppEngine application',
                                            )
        self.parser.set_defaults(func=self.run)
        

    @staticmethod
    def run(args, config):
        """Runs the build command
        
        """
        context = Context()
        context.config = config
        compile_soy_templates = CompileSoyTemplates(context)
        compile_soy_templates.then(
            GenerateSharedJsClasses()).then(
            CompileClosureApplication()).then(
            CopySourcesToBuildDirectory()).then(
            CopyDependencies()).then(
            ConfigureAppYaml()).then(
            GenerateIndexPage())

        compile_soy_templates.execute()
        


class Context(object):
    pass
        
class ExecutionStep(object):
    """Abstract class defines an execution step in the build system
    """

    def __init__(self, context=None):
        """
        """
        self.context = context
        self.next = None

    def then(self, execution_step):
        """
        """
        self.next = execution_step
        self.next.context = self.context
        return self.next
        
    def execute(self):
        """
        """
        self._execute()

        if self.next:
            self.next.execute()


    def _execute(self):
        """Abstract method
        """
        raise 'This is an abstract method and must be implemented'
        

class CompileSoyTemplates(ExecutionStep):
    """Compiles the soy template files
    """
    def _execute(self):
        """
        """
        config = self.context.config
        application_path = config.get_project_sources_path()
        generated_path = os.path.join(application_path, config.get('project', 'generated'))
        assert generated_path
    
        application_paths = [application_path]
        if config.has_section('deps'):
            application_paths += [config.get('deps', option) for option in config.options('deps')]
        soy_compiler = config.get('closure', 'soy_compiler')
    
        closure.prepare_generated_directory(generated_path=generated_path)

        compiled_successfully = closure.compile_soy_templates(
            generated_path=generated_path,
            application_path=application_path,
            application_paths=application_paths,
            SoyToJsSrcCompiler_path=soy_compiler
            )

        if compiled_successfully:
            closure.copy_required_js_files(
                generated_path,
                os.path.dirname(soy_compiler))
        

class GenerateSharedJsClasses(ExecutionStep):
    """
    """
    def _execute(self):
        """
        """
        config = self.context.config
        shared = closure.GenerateSharedJavascriptClasses(config)
        shared.run()
        

class CompileClosureApplication(ExecutionStep):
    """
    """
    def _execute(self):
        """
        """
        config = self.context.config
        sources_path = config.get_project_sources_path()
        src = [sources_path]
        print 'Finding Google Closure Entrypoint class...'
        ep = loader2.locate("entrypoint.js", src)[0]

        paths = src + list(loader2.application_paths())
        compiled_files =  os.path.join(sources_path, '%s/compiled.js' % config.get('project', 'generated'))
        
        closure.compile_closure_files(ep, paths, compiled_files)

        
class CopySourcesToBuildDirectory(ExecutionStep):
    """
    """
    def _execute(self):
        """
        """
        config = self.context.config
        application_path = config.get_project_sources_path()
        build = os.path.join(config.get_project_path(), config.get('project', 'build'))

        logging.info('Deleting build directory...')
        shutil.rmtree(build)
        logging.info('Copying appliaction sources...')
        shutil.copytree(application_path, build)
        logging.info('Done')
        
class CopyDependencies(ExecutionStep):
    """
    """
    def _execute(self):
        """
        """
        #TODO: implement the deps logic
        #if config.has_section('deps'):
        #    for dep in config.options('deps'):

        #TODO: use loader2.locate .. and copy files execluding *.js
        #For now just copy tic stuff
        logging.info('Copying Deps...')

        for f in loader2.locate('*'):
            if not re.match('.*/app.yaml$',f) and \
               not re.match('.*/index.yaml$',f) and \
               not re.match('.*/\.[^\.]+$', f) and \
               not re.match('.*/development/.*', f) and \
               not re.match('.+\.pyc$', f):

                relpath = loader2.get_relative_path(f)

                if re.match('.*/client/.*', f):
                    if f.endswith('.css'):
                        self.copy(f, relpath)
                else:
                    self.copy(f, relpath)

        logging.info('Done...')
                
    def copy(self, f, relpath):
        """
        Arguments:
        - `src`:
        - `relpath`:
        """
        config = self.context.config
        build = os.path.join(config.get_project_path(), config.get('project', 'build'))
        dist = os.path.join(build, os.path.dirname(relpath))
        try:
            os.makedirs(dist)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise
            
        logging.info('Copying %s' % f)
        shutil.copy2(f,dist)

class ConfigureAppYaml(ExecutionStep):
    """
    """
    def _execute(self):
        '''Gnerates the app.yaml file
        '''
        config = self.context.config
        build_path = os.path.join(config.get_project_path(), config.get('project', 'build'))
        self.app_yaml = os.path.join(build_path, 'app.yaml')

        app = self._read_original_app_yaml_file()
        handlers = app['handlers']
        
        static_dirs = self._get_static_dirs(build_path)
        
        insert_index = len(handlers) - 1
        for static_dir in static_dirs:
            logging.info('app.yaml: Adding static file entry %s ...' % static_dir)
            handlers.insert(insert_index,
                { 'url': '/%s' % static_dir,
                  'static_dir': static_dir
                  })

        #add the static root handler
        handlers.insert(len(handlers) - 1,
                        { 'url': '/',
                  'static_files': 'generated/index.html',
                  'upload': 'generated/index.html'
                  })
        
        out = open(self.app_yaml, 'w')
        out.write(yaml.dump(app, default_flow_style=False))
        
    def _read_original_app_yaml_file(self):
        '''Reads and returns the app.yaml file as a yaml objects.
        '''
        return yaml.load(open(self.app_yaml))
    
    def _get_static_dirs(self, build_path):
        '''finds all 'client' directories and returns them as list'''
        paths = [build_path, loader2.application_path()]
        client_dirs = set()
        for f in loader2.locate('*', [build_path]):
            if re.match('.*/client/.*', f):
                client_dirs.add(loader2.get_relative_path(os.path.dirname(f), paths))
        return client_dirs


class GenerateIndexPage(ExecutionStep):
    """
    """
    def _execute(self):
        '''Gnerates the app.yaml file
        '''
        from google.appengine.ext.webapp import template

        config = self.context.config
        sources_path = config.get_project_sources_path()
        src = [sources_path]
        paths = src + list(loader2.application_paths())
        build_path = os.path.join(config.get_project_path(), config.get('project', 'build'))
        
        files = [x for x in loader2.locate('entrypoint.js',src)]
        css_deps, js_deps = closure.calculate_deps(files[0], paths)

        file = open(os.path.join(build_path, 'generated/index.html'), 'w')
        vars = {
                'entrypoint': closure.get_namespace(files[0]),
                'js_deps': ['/generated/client/compiled.js'],
                'css_deps': css_deps
                }

        
        file.write(template.render(os.path.join(loader2.application_path(), "tic/web/templates/index_compiled.html"), vars))

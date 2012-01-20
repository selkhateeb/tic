import closurebuilder
import depstree
import depswriter
import glob
import jscompiler
import source
import logging
import os
import shutil
import types

from tic import loader
from tic.core import Component, implements
from tic.development.tools.api import IDirectoryWatcher, IRunServerTask, IBuildTask
from tic.web import cdp
from tic.utils import importlib
from tic.development.labs import coverage

from google.appengine.ext.webapp import template

def calculate_test_deps(js_test_file_path):
    """
    Calculates the dependancy files for the test
    """
    logging.info(js_test_file_path)
    js = js_test_file_path.replace(loader.root_path(), '/') + '.js'
    css_deps, js_deps = calculate_deps(js_test_file_path.replace('_test', '_test.js'))
    
    return css_deps, ['/%s' % path for path in js_deps] + [js]
    

def _calculate_deps(js_entrypoint_file_path):
    js_sources = set()
    source_files = set()
    logging.info('Scanning paths for Javascript files...')
    for js_path in loader.locate("*.js"):
        if not js_path.startswith(coverage.INSTRUMENTED_CODE_PATH):
            source_files.add(js_path)

    for js_path in source_files:
        js_sources.add(closurebuilder._PathSource(js_path))
    
    logging.info('Done')
    logging.info('Building dependency tree..')
    tree = depstree.DepsTree(js_sources)
    
    #find the namespace of entrypoint
    entrypoint_source = closurebuilder._PathSource(js_entrypoint_file_path)
    if entrypoint_source.provides:
        namespace = entrypoint_source.provides
    else:
        namespace = entrypoint_source.requires

    #namespace = [closurebuilder._PathSource(js_entrypoint_file_path).provides.pop()]
    # The Closure Library base file must go first.
    base = closurebuilder._GetClosureBaseFile(js_sources)
    deps = [base] + tree.GetDependencies(namespace)
    logging.info('Done')
    return deps

def calculate_deps(js_entrypoint_file_path):
    """TODO Documentation"""
    
    deps = _calculate_deps(js_entrypoint_file_path)

    js_deps = [loader.get_relative_path(js_source.GetPath()) for js_source in deps]

#    js_deps = ["tic/web/client/tic.js"] + js_deps
    #calculate css deps
    css_source_to_path = dict()
    for css_path in loader.locate("*.css"):
        provide = source.CssSource(source.GetFileContents(css_path)).getProvideCssRule()
        if provide:
            css_source_to_path[provide] = css_path

    css_requires = set()
    css_deps = set()
    for js_source in deps:
        css_requires.update(js_source.require_csses)

    for css_req in css_requires:
        css_deps.add(loader.get_relative_path(css_source_to_path[css_req]))


    return (css_deps, js_deps)#[loader.get_relative_path(js_source.GetPath()) for js_source in deps]

def compile_soy_templates(templates=None):
  """
  Compiles the soy files
  TODO: cannot do this in appengine dev server since os.popen is not defined
  so a better approach would be to run a deamon that that monitors the file
  system and generates all needed stuff JIT
  """ 
  
  if templates == None:
    logging.info('Scanning for soy template files...')
    template_files = set()
    for template_file in loader.locate("*.soy"):
      template_files.add(template_file)
      logging.info(template_file)

    if not template_files: 
      logging.info('No templates found.')
      return
  else:
    template_files = set(templates)

  if not template_files:
    return

  generated_path = "%sgenerated/client/templates/" % loader.root_path()
  SoyToJsSrcCompiler_path = "%s/../tools/closure-templates/SoyToJsSrcCompiler.jar" % loader.root_path()

  logging.info('Found %s template(s)' % len(template_files))

  logging.info('compiling ...')
  a = os.popen("java -jar %(soy_to_js_compiler)s --outputPathFormat %(generated_path)s%(tmp)s{INPUT_DIRECTORY}{INPUT_FILE_NAME_NO_EXT}.js %(options)s %(templates)s"
               % {'soy_to_js_compiler': SoyToJsSrcCompiler_path,
               'generated_path': generated_path,
               'tmp': 'tmp',
               'templates': ' '.join(template_files),
               'options':' '.join([
               '--shouldGenerateJsdoc',
               '--shouldProvideRequireSoyNamespaces'
               ])})
  if a.close():
    logging.info('Failed to compile... check error message')
    return

#    logging.info('Generated files:')
#    for fname in os.listdir(generated_path):
#        logging.info('\t%s%s' % (generated_path, fname))

#  src = '%stmp%s' % (generated_path, loader.root_path())
#  for directory in os.listdir(src):
#    shutil.move('%s%s' % (src,directory), generated_path)

  src_root = '%stmp' % generated_path
  for f in template_files:
    l = len(loader.root_path().split('/'))
    filename = ''.join(['.'.join(f.split('/')[l-1:]).rstrip('.soy').strip('.'), '.js'])
    src = ''.join([src_root, f.rstrip('.soy'), '.js'])
    dst = ''.join([generated_path,filename])
    logging.info(filename)
    logging.info(src)
    logging.info(dst)
    shutil.copy2(src, dst)

#    shutil.move(directory, generated_path)
    
  shutil.rmtree('%stmp' % generated_path)


  logging.info('Done.')
  return template_files

def prepare_generated_directory():
    """Documentation"""
    generated_path = "%sgenerated/client/templates/" % loader.root_path()
    try:
        shutil.rmtree(generated_path)
        os.makedirs(generated_path)
    except OSError:
        pass #no such file or dir, dir already exists 

def copy_required_js_files():
    """Documentation"""
    generated_path = "%sgenerated/client/templates/" % loader.root_path()
    
    logging.info('Copying required files...')
    jsutil_file = '%s/../tools/closure-templates/soyutils_usegoog.js' % loader.root_path()
    logging.info('\t' + jsutil_file)
    shutil.copy(jsutil_file, generated_path)

def compile_closure_files():
    """Compiles the javascript files
    """
    files = [f for f in loader.locate("entrypoint.js")]
    
    deps = _calculate_deps(files[0])
    compiled_source = jscompiler.Compile(
        "/Users/selkhateeb/Development/Projects/CarsSearchEngine/tools/closure-compiler/compiler.jar",
        [js_source.GetPath() for js_source in deps],
        ['--compilation_level=ADVANCED_OPTIMIZATIONS',
#         '--create_source_map=example-map',
         '--formatting=pretty_print',
         '--debug'
         ])
    out = open('generated/client/compiled.js', 'w')
    out.write(compiled_source)
    

class ClosureTemplatesDirectoryWatcher(Component):
    implements(IDirectoryWatcher)

    generated_path = "%sgenerated/client/templates/" % loader.root_path()

    # IDirectoryWatcher API
    def changed(self, list):
        """
        @see IDirectoryWatcher.changed
        """
        self._compile(list)
    def created(self, list):
        """
        @see IDirectoryWatcher.created
        """
        self._compile(list)
        
    def deleted(self, list):
        """
        @see IDirectoryWatcher.deleted
        """
        #TODO: delete corresponding template file
    # private
    def _pick_soy_files(self, files):
        """
        Removes all non soy files
        """
        soys = []
        for file in files:
            if file.endswith('.soy'):
                soys.append(file)
        return soys

    def _is_copy_required_js_files_required(self):
        """Determines wheather we need to copy soy js files.
        
        basically checks if soyutils_usegoog.js exists
        """
        return not os.path.exists("%ssoyutils_usegoog.js" % self.generated_path)
    def _compile(self, files):
        """
        compiles the template files
        """
        compile_soy_templates(self._pick_soy_files(files))
        if self._is_copy_required_js_files_required():
            copy_required_js_files()


class GenerateIndexPage(Component):
    implements(IBuildTask)
    
    def run(self, build_path):
        files = [x for x in loader.locate('entrypoint.js')]
        css_deps, js_deps = calculate_deps(files[0])
            
        file = open('%s/%s' % (build_path, 'generated/index.html'), 'w')
        vars = {
                'entrypoint': loader._get_module_name(files[0]),
                'js_deps': ['/generated/client/compiled.js'],
                'css_deps': css_deps
                }
        file.write(template.render("%stic/web/templates/index_compiled.html" % loader.root_path(), vars))
    
            
class CompileSoyTemplates(Component):
    implements(IBuildTask)
    def run(self, build_path):
        logging.info('Compiling Soy Templates ...')
        prepare_generated_directory()
        #if we have templates copy the required js files
        if compile_soy_templates(): 
            copy_required_js_files()
            
class CompileClosureApplication(Component):
    implements(IBuildTask)
    def run(self, build_path):
        logging.info('Compiling Javascript with google closure compiler ...')
        compile_closure_files()
            


class GenerateSharedJavascriptClasses(Component):
    implements(IRunServerTask, IDirectoryWatcher, IBuildTask)

    def __init__(self):
        self.generated_path = "%sgenerated/client/closure/" % loader.root_path()

    #---------------
    # IRunSererTask and IBuildTask implementation
    #---------------
    def run(self, build_path=None):
        
        logging.info('Generating shared js classes:')
        commands = self._get_shared_commands()
        self._prepare_generated_path()

        for command in commands:
            logging.info('\t%s.%s.js' % (command.__module__, command.__name__))
            self._generate_file_for_class(command)
            
    #----------------
    # IDirectoryWatcher implementation
    #   -changed
    #   -created
    #   -deleted
    #----------------
    def changed(self, changed_files):
        """
        changed_files: list of paths to changed files
        """
        for shared_file in changed_files:
            if '/shared.py' in shared_file:
                for command in self._get_shared_commands_for_file(shared_file):
                    self._generate_file_for_class(command)

    def created(self, created_files):
        """
        created_files: list of paths to newly created files
        """
        self.changed(created_files)

    def deleted(self, deleted_files):
        """
        deleted_files: list of paths to removed files

        TODO: This is the tricky one.. we need to delete the generated closure
        class files.

        Implementation Idea: since this is a singleton class we can keep the
        state in a variable and use it to clean up ..

        """
    

    def _get_shared_commands(self):
        shared_files = loader.locate('shared.py')
        commands = set()
        for file in shared_files:
            commands.update(self._get_shared_commands_for_file(file))

        return commands

    def _get_shared_commands_for_file(self, file):
        commands = []
        module_name = loader._get_module_name(file)
        module = importlib.import_module(module_name)
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, (type, types.ClassType)) and
                issubclass(obj, cdp.Command)):
                commands.append(obj)
        return commands

    def _generate_file_for_class(self, command_class):
        filename = '%s.%s' % (command_class.__module__, command_class.__name__)
        file = open('%s%s.js' % (self.generated_path, filename), "w")
        file.write(command_class('closure').to_js())
        file.close()

    def _prepare_generated_path(self):
        try:
            shutil.rmtree(self.generated_path)
        except OSError:
            pass #no such file or dir
        os.makedirs(self.generated_path)

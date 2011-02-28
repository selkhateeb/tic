import glob
import logging
import os
import shutil

import closurebuilder
import depstree
from tic import loader
from tic.core import Component
from tic.core import implements
from tic.tools.api import IDirectoryWatcher
import depswriter
def calculate_test_deps(js_test_file_path):
    """
    Calculates the dependancy files for the test
    """
    js = js_test_file_path.replace(loader.root_path(), '/') + '.js'
    css_deps, js_deps = calculate_deps(js_test_file_path.replace('_test', '.js'))

    return css_deps, ['/%s' % path for path in js_deps] + [js]

def calculate_deps(js_entrypoint_file_path):
    """TODO Documentation"""
    
    js_sources = set()
    source_files = set()
    logging.info('Scanning paths...')
    for js_path in loader.locate("*.js"):
        source_files.add(js_path)
    
    for js_path in source_files:
        js_sources.add(closurebuilder._PathSource(js_path))

    logging.info('Building dependency tree..')
    tree = depstree.DepsTree(js_sources)
    namespace = [loader._get_module_name(js_entrypoint_file_path)]
    # The Closure Library base file must go first.
    base = closurebuilder._GetClosureBaseFile(js_sources)
    deps = [base] + tree.GetDependencies(namespace)

    js_deps = [loader.get_relative_path(js_source.GetPath()) for js_source in deps]

    js_deps = ["tic/web/client/tic.js"] + js_deps
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
    system and generates all needed stuff
    """
    
    if templates == None:
        logging.info('Scanning for soy template files...')
        template_files = set()
        for template_file in loader.locate("*.soy"):
            template_files.add(template_file)

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
    a = os.popen("java -jar %(soy_to_js_compiler)s --outputPathFormat %(generated_path)s{INPUT_FILE_NAME_NO_EXT}.js %(options)s %(templates)s"
                 % {'soy_to_js_compiler': SoyToJsSrcCompiler_path,
                 'generated_path': generated_path,
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




    
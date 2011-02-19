import depstree
import jscompiler
import source
import treescan
import closurebuilder
import logging
from tic import loader

def calculate_deps(js_entrypoint_file_path):
    """TODO Documentation"""
    
    sources = set()
    source_files = set()
    logging.info('Scanning paths...')
    for js_path in loader.locate("*.js"):
        source_files.add(js_path)

    for js_path in source_files:
        sources.add(closurebuilder._PathSource(js_path))

    logging.info('Building dependency tree..')
    tree = depstree.DepsTree(sources)

    namespace = [loader._get_module_name(js_entrypoint_file_path)]

    # The Closure Library base file must go first.
    base = closurebuilder._GetClosureBaseFile(sources)
    deps = [base] + tree.GetDependencies(namespace)

    return [loader.get_relative_path(js_source.GetPath()) for js_source in deps]

def compile_soy_templates():
    """
    Compiles the soy files
    TODO: cannot do this in appengine dev server since os.popen is not defined
    so a better approach would be to run a deamon that that monitors the file
    system and generates all needed stuff
    """
    import os
    import shutil
    import glob
    logging.info('Scanning for soy template files...')
    template_files = set()
    for template_file in loader.locate("*.soy"):
        template_files.add(template_file)

    if not template_files:
        logging.info('No templates found.')
        return

    generated_path = "%sgenerated/templates/" % loader.root_path()

    logging.info('Found %s template(s)' % len(template_files))

    shutil.rmtree(generated_path)
    os.makedirs(generated_path)

    logging.info('compiling ...')
    a = os.popen("java -jar /Users/selkhateeb/Development/Projects/tic/tools/closure-templates/SoyToJsSrcCompiler.jar --outputPathFormat %(generated_path)s{INPUT_FILE_NAME_NO_EXT}.js %(options)s %(templates)s"
                 % {'generated_path': generated_path,
                 'templates': ' sdfas'.join(template_files),
                 'options':' '.join([
                    '--shouldGenerateJsdoc',
                    '--shouldProvideRequireSoyNamespaces'
                 ])})
    if a.close():
        logging.info('Failed to compile... check error message')
        return

    logging.info('Generated files:')
    for fname in os.listdir(generated_path):
        logging.info('\t%s%s' % (generated_path,fname))

    logging.info('Copying required files...')
#    for file in glob.glob('/Users/selkhateeb/Development/Projects/tic/tools/closure-templates/*.js'):
    jsutil_file = '/Users/selkhateeb/Development/Projects/tic/tools/closure-templates/soyutils_usegoog.js'
    logging.info('\t' + jsutil_file)
    shutil.copy(jsutil_file, generated_path)
    logging.info('Done.')

    
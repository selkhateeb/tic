import depstree
import jscompiler
import source
import treescan
import closurebuilder
import logging
from tic import loader

def calaculateDeps(js_entrypoint_file_path):
    """TODO Documentation"""
    sources = set()
    source_files = set()
    logging.info('Scanning paths...')
    paths = [
    '/Users/sam/Development/Projects/Personal/tic/src/tic/web/client/frameworks/closure-lib/closure/goog/',
    '/Users/sam/Development/Projects/Personal/tic/src/tic/web/client/frameworks/closure-lib/third_party/closure/goog/',
    '%s/example/' % loader.root_path()]
    for path in paths:
        for js_path in treescan.ScanTreeForJsFiles(path):
            source_files.add(js_path)
    #    for js_path in loader.locate("*.js"):

    for js_path in source_files:
        sources.add(closurebuilder._PathSource(js_path))
    
    logging.info('Building dependency tree..')
    tree = depstree.DepsTree(sources)

    logging.info("#####################:    %s" % loader._get_module_name(js_entrypoint_file_path))
    namespace = [loader._get_module_name(js_entrypoint_file_path)]

    # The Closure Library base file must go first.
    base = closurebuilder._GetClosureBaseFile(sources)
    logging.info(namespace)
    deps = [base] + tree.GetDependencies(namespace)

    for a in deps:
        logging.info("aaaaaaaaaaaaaaaaaaaaaa:%s" % a )

    return ''.join([js_source.GetPath() for js_source in deps])
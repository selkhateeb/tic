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

#Runs what ever in __all__ before it runs the server

import os
import threading
import logging
from tic.development import closure
from tic.development.tools import directory_watcher
from tic.development.labs import coverage

__all__ = ['compile_soy', 'generate_shared_files',
            'generate_insrtumentation_code', 'watch_directories']


soy_compiler_path = '/Users/selkhateeb/Development/Projects/tic/tools/closure-templates'

def compile_soy(config=None):
    application_path = config.get_project_sources_path()
    generated_path = os.path.join(application_path, config.get('project', 'generated'))
    assert generated_path
    
    application_paths = [application_path]
    if config.has_section('deps'):
        application_paths += [config.get('deps', option) for option in config.options('deps')]
        
    
    soy_compiler = os.path.join(soy_compiler_path, 'SoyToJsSrcCompiler.jar')
    
        
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
            soy_compiler_path)
    

def watch_directories(config=None):
    application_path = config.get_project_sources_path()
    generated_path = os.path.join(application_path, config.get('project', 'generated'))
    assert generated_path

    application_paths = [application_path]
    if config.has_section('deps'):
        application_paths += [config.get('deps', option) for option in config.options('deps')]
        
    
    soy_compiler = os.path.join(soy_compiler_path, 'SoyToJsSrcCompiler.jar')

    def f(created, changed, removed):
        for f in created:
            if f.endswith('.soy'):
                compiled_successfully = closure.compile_soy_templates(
                    template_files=[f],
                    generated_path=generated_path,
                    application_path=application_path,
                    application_paths=application_paths,
                    SoyToJsSrcCompiler_path=soy_compiler)

        for f in changed:
            if f.endswith('.soy'):
                compiled_successfully = closure.compile_soy_templates(
                    template_files=[f],
                    generated_path=generated_path,
                    application_path=application_path,
                    application_paths=application_paths,
                    SoyToJsSrcCompiler_path=soy_compiler)

        for f in removed:
            logging.info('removed:%s', f)
        return True

    try:
        p = threading.Thread(
            target=directory_watcher.watch_directories,
            args=([config.get_project_sources_path()],f, 1))
        p.start()
    
    except KeyboardInterrupt:
        p.join()

def generate_shared_files(config=None):
    shared = closure.GenerateSharedJavascriptClasses(config)
    shared.run()


def generate_insrtumentation_code(config=None):
    """generates instrumenteation code for test files
   """
    application_path = config.get_project_sources_path()

    tests_path = os.path.join(
        config.get_project_path(),
        config.get('project', 'tests')) 

    
    generated_path = os.path.join(tests_path, config.get('project', 'instrumented'))

    #find the files ending with _test.js
    from tic import loader2
    for f in loader2.locate('*_test.js', paths=[tests_path]):
        print f
        file = os.path.join(config.get_project_sources_path(), os.path.relpath(f.replace('_test.js', '.js'), tests_path))
        
        coverage.generate_instrumented_file(
            file,
            node_executable = 'node',
            node_script = os.path.join(os.path.dirname(coverage.__file__), 'main.js'),
            instrumented_code_path = generated_path)


#Runs what ever in __all__ before it runs the server

import os
from tic.development import closure
__all__ = ['compile_soy']


soy_compiler_path = '/Users/selkhateeb/Development/Projects/tic/tools/closure-templates'

def compile_soy(config=None):
    application_path = config.get_project_sources_path()
    generated_path = os.path.join(application_path, config.get('tic', 'generated'))
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
    

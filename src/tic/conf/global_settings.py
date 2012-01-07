
# Ordered list of filters to apply to all requests
REQUEST_FILTERS = ()

# Name of the component that handles requests to the base URL.
DEFAULT_HANDLER = "tic.web.main.DefaultHandler"


# What javascript lib should we use..
# Possible values:
#       - 'closure' => Google Closure library
#       - 'dojo' => Dojo ToolKit
#       - 'autodetect' => Automatically finds out by looking at the entrypoint.js file
JAVASCRIPT_TOOLKIT = 'autodetect'

# ordered list of components that implements an interface
# if the component is not in the list, it will be appended to the bottom of the
# list
EXTENSION_POINTS = {
  'tic.development.tools.api.IRunServerTask':(
    'tic.development.closure.GenerateSharedJavascriptClasses',
    'tic.development.appengine.server.StartWatchingForDirectoryChangesTask',
    ),
  'tic.development.tools.api.IBuildTask':(
        'tic.development.tools.BuildTaskRunner',
        'tic.development.closure.GenerateSharedJavascriptClasses',
        'tic.development.closure.CompileSoyTemplates',
        'tic.development.closure.CompileClosureApplication',
        'tic.development.tools.CopySourceTreeBuildTask',
        'tic.development.closure.GenerateIndexPage',
        'tic.development.tools.DeleteDevelopmentFiles',
        )
}

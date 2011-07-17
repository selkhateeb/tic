
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
  'tic.tools.api.IRunServerTask':(
    'tic.web.cdp.closure.GenerateSharedJavascriptClasses',
    'tic.appengine.development.server.StartWatchingForDirectoryChangesTask',
    ),
  'tic.tools.api.IBuildTask':(
        'tic.tools.BuildTaskRunner',
        'tic.web.cdp.closure.GenerateSharedJavascriptClasses',
        'tic.web.cdp.closure.CompileSoyTemplates',
        'tic.web.cdp.closure.CompileClosureApplication',
        'tic.tools.CopySourceTreeBuildTask',
        'tic.web.cdp.closure.GenerateIndexPage',
        'tic.tools.DeleteDevelopmentFiles',
        )
}

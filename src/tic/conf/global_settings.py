
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
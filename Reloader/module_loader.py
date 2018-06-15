import imp, os, sys

def load ( moduleDirectories, pluginGlobals ):

	moduleExtensions  = [ "py" ]
	moduleLoader_Name = "module_loader"
	modulePaths       = []

	for path in sys.path:
		print(path)
		if path.endswith ( "Sublime Text 3" + os.sep + "Installed Packages" + os.sep + "servicenow-sync.sublime-package" ):
			packagesPath = path
			break

	for directory in moduleDirectories:
		modulePaths.append ( packagesPath + os.sep + directory )

	for index in range ( 0, 2 ):
		for path in modulePaths:
			for file in os.listdir ( path ):
				for extension in moduleExtensions:

					if file.endswith ( os.extsep + extension ):
						moduleName = os.path.basename( file )[ : - len ( os.extsep + extension ) ]

						if moduleName != moduleLoader_Name:
							fileObject, file, description = imp.find_module( moduleName, [ path ] )
							pluginGlobals[ moduleName ] = imp.load_module ( moduleName, fileObject, file, description )
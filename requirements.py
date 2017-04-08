def install_requirements(package):
	import importlib
	try:
		imortlib.import_module(package)
	except ImportError as e:
		import pip
		pip.main(['install', package])
	finnaly:
		print("Installed {package}")

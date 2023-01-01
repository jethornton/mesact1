
def save_settings(parent):
	parent.settings.setValue('window size', parent.size())
	parent.settings.setValue('window position', parent.pos())

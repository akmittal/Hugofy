import sublime, sublime_plugin, subprocess, os, shlex

def setvars():
	global settings, path, sitename, repository
	settings = sublime.load_settings("hugofy.sublime-settings")
	path = settings.get("Directory")
	sitename = settings.get("Sitename")
	repository = settings.get("Repository")
	if not os.path.exists(os.path.join(path, sitename)):
		 os.makedirs(os.path.join(path, sitename))
	os.chdir(os.path.join(path,sitename))

class HugonewsiteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		setvars()
		process = "hugo new site " + os.path.join(path, sitename)
		subprocess.Popen(shlex.split(process))

class HugonewcontentCommand(sublime_plugin.TextCommand):
	def on_done(self, pagename):
		if not pagename:
			sublime.error_message("No filename provided")
		process = "hugo new " + pagename
		subprocess.Popen(shlex.split(process))
		sublime.active_window().open_file(os.path.join(path, sitename, "content", pagename))
	def on_change(self,filename):
		pass
	def on_cancel(self):
		sublime.error_message("No filename provided")
	def run(self,edit):
		setvars()
		sublime.active_window().show_input_panel("Enter file name", "", self.on_done, self.on_change, self.on_cancel)

class HugoversionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			out = subprocess.check_output(["hugo", "version"], stderr=subprocess.STDOUT,universal_newlines=True)
			sublime.message_dialog(out)
		except:
			sublime.error_message("Hugo not installed or path not set")

class HugoserverstartCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		setvars()
		server = settings.get("Server")
		theme = settings.get("DefaultTheme")
		try:
			startCmd = "hugo server --theme={} --buildDrafts --watch --port={}".format(theme, server["PORT"])
			out = subprocess.Popen(shlex.split(startCmd), stderr=subprocess.STDOUT, universal_newlines=True)
			sublime.status_message('Server Started: {}'.format(startCmd))
		except:
			sublime.error_message("Error starting server")

class HugoserverstopCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		setvars()
		try:
			stopCmd1 = "ps aux "
			stopCmd2 = " grep 'hugo server' "
			stopCmd3 = " grep -v grep "
			stopCmd4 = " awk '{}' ".format('{ print "kill -9", $2 }')
			stopCmd5 = " sh"
			out1 = subprocess.Popen(shlex.split(stopCmd1), stdout=subprocess.PIPE, universal_newlines=True)
			out2 = subprocess.Popen(shlex.split(stopCmd2), stdout=subprocess.PIPE, stdin=out1.stdout, universal_newlines=True)
			out3 = subprocess.Popen(shlex.split(stopCmd3), stdout=subprocess.PIPE, stdin=out2.stdout, universal_newlines=True)
			out4 = subprocess.Popen(shlex.split(stopCmd4), stdout=subprocess.PIPE, stdin=out3.stdout, universal_newlines=True)
			out5 = subprocess.Popen(shlex.split(stopCmd5), stdin=out4.stdout, universal_newlines=True)
			out1.stdout.close()
			out2.stdout.close()
			out3.stdout.close()
			out4.stdout.close()
			sublime.status_message('Server Stoped: Killed')
		except:
			sublime.error_message("Error stoping server")

class HugobuildCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		try:
			buildCmd = "hugo --buildDrafts"
			out = subprocess.Popen(shlex.split(buildCmd),stdout=subprocess.PIPE)
			# print(out.communicate()[0].decode('utf-8'))
			sublime.message_dialog(out.communicate()[0].decode('utf-8'))
		except:
			sublime.error_message("Hugo not installed")

class HugogetthemesCommand(sublime_plugin.TextCommand):
	"""download themes for hugo"""
	def run(self, edit):
		setvars()
		try:
			getthemesCmd = "git clone --recursive https://github.com/spf13/hugoThemes.git " + os.path.join(path, sitename, "themes")
			out = subprocess.Popen(shlex.split(getthemesCmd), stderr=subprocess.STDOUT, universal_newlines=True)
		except:
			sublime.error_message("git not installed or path not set")

class HugosetthemeCommand(sublime_plugin.TextCommand):
	def on_done(self, themename):
		if not themename:
			sublime.error_message("No theme name provided")
		else:
			settings.set("DefaultTheme", themename)
			sublime.save_settings("hugofy.sublime-settings")

	def on_change(self, themename):
		pass
	def on_cancel(self):
		pass

	def run(self, edit):
		setvars()
		sublime.active_window().show_input_panel("Enter theme name", "", self.on_Pdone, self.on_change, self.on_cancel)

class HugodeployCommand(sublime_plugin.TextCommand):
	"""deploy public directory to GitHub Pages"""
	def on_done(self, commit_message=''):
		try:
			script_path = os.path.join(sublime.packages_path(), 'Hugofy/deploy.sh')
			deployCmd = "sh '{}' -r '{}' -m '{}' -d '{}'".format(script_path, repository, commit_message, os.path.join(path, sitename))
			sublime.status_message(deployCmd)
			out = subprocess.Popen(shlex.split(deployCmd), universal_newlines=True)
			out.wait()
			sublime.message_dialog('Success!')
		except:
			sublime.error_message("git not installed or path not set")

	def on_change(self,filename):
		pass
	def on_cancel(self):
		sublime.error_message("No Commit Message provided")
	def run(self,edit):
		setvars()
		sublime.active_window().show_input_panel("Enter Commit Message", "", self.on_done, self.on_change, self.on_cancel)


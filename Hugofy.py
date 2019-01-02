import sublime, sublime_plugin, subprocess, os


def setvars():
    global settings, path, sitename
    settings = sublime.load_settings("hugofy.sublime-settings")
    path = settings.get("Directory")
    sitename = settings.get("Sitename")
    if not os.path.exists(os.path.join(path, sitename)):
        os.makedirs(os.path.join(path, sitename))
    os.chdir(os.path.join(path, sitename))


class HugonewsiteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setvars()
        process = ["hugo", "new", "site", os.path.join(path, sitename)]
        subprocess.Popen(process)


class HugonewcontentCommand(sublime_plugin.TextCommand):
    def on_done(self, pagename):
        if not pagename:
            sublime.error_message("No filename provided")
        process = ["hugo", "new", pagename]
        subprocess.Popen(process)
        sublime.active_window().open_file(
            os.path.join(path, sitename, "content", pagename)
        )

    def on_change(self, filename):
        pass

    def on_cancel(self):
        sublime.error_message("No filename provided")

    def run(self, edit):
        setvars()
        sublime.active_window().show_input_panel(
            "Enter file name", "", self.on_done, self.on_change, self.on_cancel
        )


class HugoversionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            out = subprocess.check_output(
                ["hugo", "version"], stderr=subprocess.STDOUT, universal_newlines=True
            )
            sublime.message_dialog(out)
        except:
            sublime.error_message("Hugo not installed or path not set")


class HugoserverCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setvars()
        server = settings.get("Server")
        startCmd = ["hugo", "server"]
        if server["THEME_FLAG"]:
            startCmd = startCmd + ["--theme={}".format(server["THEME"])]
        if server["DRAFTS_FLAG"]:
            startCmd = startCmd + ["--buildDrafts"]

        startCmd = startCmd + ["--watch", "--port={}".format(server["PORT"])]

        try:
            out = subprocess.Popen(
                startCmd, stderr=subprocess.STDOUT, universal_newlines=True
            )
            sublime.status_message("Server Started: {}".format(startCmd))
        except:
            sublime.error_message("Error starting server")


class HugobuildCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            out = subprocess.Popen(["hugo", "--buildDrafts"], stdout=subprocess.PIPE)
            # print(out.communicate()[0].decode('utf-8'))
            sublime.message_dialog(out.communicate()[0].decode("utf-8"))
        except:
            sublime.error_message("Hugo not installed")


class HugogetthemesCommand(sublime_plugin.TextCommand):
    """download themes for hugo"""

    def run(self, edit):
        setvars()
        try:
            out = subprocess.Popen(
                [
                    "git",
                    "clone",
                    "--recursive",
                    "https://github.com/spf13/hugoThemes.git",
                    os.path.join(path, sitename, "themes"),
                ],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
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
        sublime.active_window().show_input_panel(
            "Enter theme name", "", self.on_done, self.on_change, self.on_cancel
        )

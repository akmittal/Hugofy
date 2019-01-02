import sublime, sublime_plugin, subprocess, os
from contextlib import contextmanager


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def setvars():
    global settings, path, sitename
    settings = sublime.load_settings("hugofy.sublime-settings")
    path = sublime.active_window().folders()[0]


class HugonewcontentCommand(sublime_plugin.TextCommand):
    def on_done(self, pagename):
        if not pagename:
            sublime.error_message("No filename provided")
        process = ["hugo", "new", pagename]
        with cwd(path):
            subprocess.Popen(process)
        sublime.active_window().open_file(os.path.join(path, "content", pagename))

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
        # server = settings.get("Server")

        start_cmd = ["hugo", "server"]
        port = settings.get("PORT")

        if settings.get("DRAFTS_FLAG"):
            start_cmd = start_cmd + ["--buildDrafts"]

        start_cmd = start_cmd + ["--watch", "--port=%s" % port]

        try:
            with cwd(path):
                out = subprocess.Popen(
                    start_cmd, stderr=subprocess.STDOUT, universal_newlines=True
                )
            sublime.status_message("Server started: {}".format(start_cmd))
        except Exception as e:
            sublime.error_message("Error starting server: {}".format(e))


class HugobuildCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            with cwd(path):
                out = subprocess.Popen(
                    ["hugo", "--buildDrafts"], stdout=subprocess.PIPE
                )
            # print(out.communicate()[0].decode('utf-8'))
            sublime.message_dialog(out.communicate()[0].decode("utf-8"))
        except Exception as e:
            sublime.error_message("Exception caught {}".format(e))


class HugogetthemesCommand(sublime_plugin.TextCommand):
    """Download all themes for Hugo."""

    def run(self, edit):
        setvars()
        try:
            out = subprocess.Popen(
                [
                    "git",
                    "clone",
                    "--recursive",
                    "https://github.com/spf13/hugoThemes.git",
                    os.path.join(path, "themes"),
                ],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        except:
            sublime.error_message("git not installed or path not set")

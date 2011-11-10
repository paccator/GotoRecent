import sublime, sublime_plugin, os

class GotoRecentListener(sublime_plugin.EventListener):
  def on_deactivated(self, view):
    if view.file_name():
      view.window().run_command("goto_recent", { "file_name": view.file_name() })

class GotoRecentCommand(sublime_plugin.WindowCommand):
  def __init__(self, window):
    sublime_plugin.WindowCommand.__init__(self, window)
    self.recent_files = []
    self.enabled      = True

  def unshift(self, file_name):
    item = [os.path.basename(file_name), file_name]

    for _ in range(self.recent_files.count(item)):
      self.recent_files.remove(item)

    self.recent_files.insert(0, item)

  def selected(self, index):
    if index >= 0:
      target_file = self.recent_files[index][1]
      
      if self.window.active_view():
        current_file = self.window.active_view().file_name()
        self.unshift(current_file)

      self.window.open_file(target_file)

    self.enabled = True

  def run(self, file_name=None):
    if self.enabled:
      if file_name:
        self.unshift(file_name)
      else:
        self.enabled = False
        self.window.show_quick_panel(self.recent_files, self.selected)

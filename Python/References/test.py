from tkinter import Tk, Frame, BOTH, Menu, Label, SUNKEN, X, BOTTOM

class Application(Frame):
   def __init__(self, parent):
      Frame.__init__(self, parent, background = "white")
      parent.configure(bg = "black")
      self.pack(fill = BOTH, expand = True, padx = 20, pady = 20)

      self.parent = parent

      # Maximize window
      self.screenWidth = self.parent.winfo_screenwidth() - 5
      self.screenHeight = self.parent.winfo_screenheight() - 110
      self.parent.geometry('%dx%d+%d+%d' % (self.screenWidth, self.screenHeight, 0, 0))
      self.parent.resizable(0, 0)

      # Status bar
      self.statusBar = StatusBar(self.parent)
      self.statusBar.pack(side = BOTTOM, fill = X)

      # Menu bar
      menubar = Menu(self.parent)
      self.parent.config(menu = menubar)

      self.commandMenu = Menu(menubar, tearoff = 0)
      self.commandMenu.add_command(label = "Rename", command = self.onRename)
      menubar.add_cascade(label = "Command", menu = self.commandMenu)

      self.helpMenu = Menu(menubar, tearoff = 0)
      self.helpMenu.add_command(label = "About", command = self.onAbout)
      menubar.add_cascade(label = "Help", menu = self.helpMenu)

   def onRename(self):
      pass
   def onAbout(self):
      pass

class StatusBar(Frame):
   def __init__(self, master):
      Frame.__init__(self, master)
      self.label = Label(self, bd = 1, relief = SUNKEN, anchor = "w")
      self.label.pack(fill=X)
   def set(self, format0, *args):
      self.label.config(text = format0 % args)
      self.label.update_idletasks()
   def clear(self):
      self.label.config(text="")
      self.label.update_idletasks()

def main():
   root = Tk()
   Application(root)
   root.mainloop()

if __name__ == '__main__':
   main()  
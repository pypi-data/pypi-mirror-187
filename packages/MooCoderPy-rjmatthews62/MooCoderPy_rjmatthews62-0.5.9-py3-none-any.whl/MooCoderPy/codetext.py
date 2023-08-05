from cgitb import text
from tkinter import messagebox, simpledialog
from ScrollText import *
from tkinter import *
from time import *
from findreplacedialog import *
import re

class CodeText(ScrollText):
    bottom:Frame
    test:Entry
    caption:str
    testvar:StringVar
    labelvar:StringVar
    modifying=False
    lastfind:str=""
    popup:Menu
    tw=None #Terminal window.
    mode:int=0
    syntax:bool=True
    syntaxlist=set()
    upload:str=""
    linenos:Label=None

    KEYWORDLIST=('if','then','else','elseif','for',
           'while','endfor','endwhile','endif',
           'try','except','finally','endtry','break','continue','in','fork','endfork')
    
    COLORLIST=("white","lawn green","cyan","magenta","orange","yellow")
    OPENBRACKETS=("(","{","[")
    CLOSEBRACKETS=(")","}","]")
    MODE_CODE = 1 # Code editor, from verb list, syntax highlight.
    MODE_EDIT = 2 # Local Edit 
    MODE_PROPERTY = 3 # Property editor (from Proplist)

    def __init__(self, parent, mode:int, **kwargs):
        super().__init__(parent, **kwargs)
        self.textbox.pack_forget()
        if self.hscroll:
            self.hscroll.pack_forget()
        self.labelvar=StringVar()
        lbl = Label(self,textvariable=self.labelvar,font="Arial 12")
        lbl.pack(side=TOP,fill=X)
        self.linenosvar=StringVar()
        self.linenos=Label(self,textvariable=self.linenosvar, font=self.textbox["font"], background="Silver", foreground="Black",width=4,justify=RIGHT)
        self.linenos.pack(side=LEFT, anchor=NE,padx=0)
        self.textbox.pack(fill=BOTH, expand=True)
        self.bottom = Frame(self, bg="LightGray")
        self.bottom.pack(side=BOTTOM, fill=X)
        if self.hscroll:
            self.hscroll.pack(side=BOTTOM, fill=X)
        self.posvar=StringVar()
        self.posvar.set("000.000")
        poslbl=Label(self.bottom,textvariable=self.posvar)
        poslbl.pack(side=LEFT)
        lbl=Label(self.bottom,text="Test ",font="Arial 12")
        lbl.pack(side=LEFT)
        self.testvar=StringVar()
        self.test=Entry(self.bottom,width=60,font="Arial 12",textvariable=self.testvar)
        self.test.pack(side=LEFT,fill=X,expand=True)
        self.setcolors()
        self.textbox.bind("<ButtonRelease>",self.trackLocation)
        self.textbox.bind("<KeyRelease>",self.trackLocation)
        self.textbox.bind("<Enter>",self.trackLocation)
        self.textbox.bind("<Control-Key-G>",self.gotoLine)
        self.textbox.bind("<Control-Key-g>",self.gotoLine)
        self.textbox.bind("<<Modified>>",self.modified)
        self.textbox.bind("<Control-Key-F>",self.find)
        self.textbox.bind("<Control-Key-f>",self.find)
        self.textbox.bind("<Control-Key-R>",self.refresh)
        self.textbox.bind("<Control-Key-r>",self.refresh)
        self.textbox.bind("<F3>",self.findAgain)
        self.textbox.bind("<<Paste>>",self.cutPaste)
        self.textbox.bind("<<Cut>>",self.cutPaste)
        self.mode=mode
        self.buildPopup()
        self.textbox.bind("<Button-3>",self.doPopup)
        self.textbox.bind("<Button-2>",self.doPopup) # For Mac, in theory.
        self.textbox.configure(undo=True,exportselection=False,inactiveselectbackground=self.textbox["selectbackground"])
        self.textbox.bind("<Return>",self.handleIndent)
        self.textbox["yscrollcommand"]=self.handleScroll

    def handleScroll(self,first,last):
        self.scrollbar.set(first,last)
        self.updateLineNos()

    def handleIndent(self,event:Event):
        line=self.textbox.get("insert linestart","insert lineend")
        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0
        self.textbox.insert(INSERT,"\n"+(" " * current_indent))
        return "break"
    
    def setFontSize(self, newsize: int):
        super().setFontSize(newsize)
        if self.linenos:
            self.linenos.configure(font=self.fontctl)

    def cutPaste(self,event:Event):
        """Trigger highlight on cut and paste."""
        self.textbox.after(0,self.highlight,True)

    def buildPopup(self):
        """Make the Popup menu"""
        p=Menu(self,tearoff=0,font="Arial 12")
        p.add_command(label="Goto Line Ctrl+G",command=self.gotoLine,underline=0)
        p.add_command(label="Find Ctrl+F",command=self.find,underline=0)
        p.add_command(label="Find Again F3",command=self.findAgain,underline=6)
        p.add_command(label="Replace Ctrl+H",command=self.doReplace, underline=1)
        self.textbox.bind("<Control-H>",self.doReplace)
        self.textbox.bind("<Control-h>",self.doReplace)
        p.add_command(label="Refresh Ctrl+R",command=self.refresh,underline=0)
        p.add_command(label="Undo Last Edit Ctrl+Z",command=self.undo)
        self.textbox.bind("<Control-z>",self.undo)
        self.textbox.bind("<Control-Z>",self.undo)
        p.add_command(label="Redo Last Edit Shift+Ctrl+Z",command=self.redo)
        self.textbox.bind("<Shift-Control-z>",self.redo)
        self.textbox.bind("<Shift-Control-Z>",self.redo)
        p.add_command(label="Redo Syntax",command=lambda: self.highlight(True),underline=10)
        p.add_command(label="Close",command=self.close,underline=0)
        if self.mode==CodeText.MODE_PROPERTY:
            p.add_command(label="Edit as Text",command=self.flattenText,underline=3)
        self.popup=p
    
    def warn(self,text:str):
            messagebox.showwarning("MooCoderPy",text)

    def flattenText(self):
        text=self.getText().split("\n")
        if len(text)<2 or not text[0].startswith("{"):
            self.warn("Not a list.")
            return
        text=text[1:-1]
        if text[-1]=="}":
            text=text[:-1]
        for (k,line) in enumerate(text):
            line=line.strip()
            if line.startswith('"'):
                line=line[1:]
            if line.endswith(","):
                line=line[:-1]
            if line.endswith('"'):
                line=line[:-1]
            line=line.replace(r'\"','"')
            text[k]=line
        self.syntax=False
        self.setText("\n".join(text))

    def close(self):
        """Close this window"""
        self.destroy()

    def setLabel(self,atext):
        self.labelvar.set(atext)

    def undo(self,event:Event=None):
        try:
            self.textbox.edit_undo()
        except:
            pass

    def redo(self,event:Event=None):
        try:
            self.textbox.edit_redo()
        except:
            pass

    def setText(self,text):
        """Populate text. Does highlighting etc"""
        self.textbox.delete("1.0",END)
        self.textbox.insert("1.0",text)
        self.textbox.edit_reset()
        self.highlight(True)

    def doPopup(self,event:Event):
        """Do the actual popup"""
        try:
            self.popup.post(event.x_root,event.y_root)
        finally:
            self.popup.grab_release()
    
    def refresh(self,event=None):
        """Refresh from server"""
        if not self.tw:
            messagebox.showwarning("MooCoderPy","No Connection to Server")
            return
        if (self.mode==self.MODE_EDIT):
            if self.upload=="":
                messagebox.showerror("MooCoderPy","No upload command.")
            else:
                self.tw.sendCmd("@edit "+self.caption)
        elif self.mode==self.MODE_PROPERTY:
            self.tw.doRefreshProperty(self.caption)
        else:
            self.tw.doRefresh(self.caption)
        return "break"

    def currentLine(self)->int:
        """Return currently selected line no"""
        return int(self.textbox.index(INSERT).split(".")[0])

    def modified(self, event):
        if not(self.modifying): # Avoid recursion
            try:
                self.modifying=True
                lno=self.currentLine()
                self.syntaxHighlight(lno-1)
                self.syntaxHighlight(lno)
                self.syntaxHighlight(lno+1)
                # Set 'modified' to 0.  This will also trigger the <<Modified>>
                # virtual event which is why we need the sentinel.
                self.textbox.edit_modified(False)
            finally:
                # Clean the sentinel.
                self.modifying = False

    def trackLocation(self,event=None):
        """Update Cursor Location"""
        loc=self.textbox.index(INSERT)
        (x,y)=loc.split(".")
        offset=1 if self.tabtype==CodeText.MODE_CODE else 0
        s="%4d:%3d" % (int(x)-offset,int(y))
        self.posvar.set(s)
        if (self.lastfind!="" and self.lastfind!=loc):
            self.textbox.tag_remove("found","1.0",END)
        self.bracketMatching()

    def updateLineNos(self):
        topix=int(self.textbox.index("@0,0").split(".")[0])
        height=int(self.textbox.winfo_height()/self.fontctl.metrics("linespace"))
        offset=1 if self.tabtype==CodeText.MODE_CODE else 0
        self.linenosvar.set("\n".join([str(x+topix-offset) for x in range(height)]))
        self.highlight()

    def bracketMatching(self):
        """Match bracket types"""
        ix=self.textbox.index(INSERT)
        c=self.textbox.get(ix)
        self.textbox.tag_remove("bracket","1.0",END)
        if c in self.OPENBRACKETS:
            text=self.textbox.get(ix,END)
            bracketlen=self.bracketMatch(c,text,True)
            if bracketlen>0:
                self.textbox.tag_add("bracket",ix,("%s +%d chars" % (ix,bracketlen)))
        elif c in self.CLOSEBRACKETS:
            text=self.textbox.get("1.0",ix+" +1 chars")
            bracketlen=self.bracketMatch(c,text,False)
            if bracketlen>0:
                self.textbox.tag_add("bracket","%s -%d chars" % (ix,bracketlen-1),ix+" +1 chars")

    
    def bracketMatch(self,bracket:str,text:str, forwards:bool)->int:
        """Routine to actually track the brackets. Returns the number of characters, 0 if not found. """
        if forwards:
            close=self.CLOSEBRACKETS[self.OPENBRACKETS.index(bracket)]
        else:
            close=self.OPENBRACKETS[self.CLOSEBRACKETS.index(bracket)]
            text=text[::-1] # Reverse
        result=0
        match=0
        for xx in text:
            result+=1
            if (xx==bracket):
                match+=1
            elif (xx==close):
                match-=1
                if (match<=0):
                    return result
        return 0

    def gotoLine(self,event=None):
        """Ask User to go to line no"""
        lno=int(self.textbox.index(CURRENT).split(".")[0])-1
        lno=simpledialog.askinteger("MooCoderPy","Go to Line No:",initialvalue=lno)
        if lno==None:
            return
        lno=min(max(lno,0),self.lastLine())
        mark="%d.0"%(lno+1)
        self.textbox.mark_set(INSERT,mark)
        self.textbox.see(mark)
    
    def find(self,event=None):
        """Find text in editor"""
        findReplaceSettings.isreplace=False
        FindReplaceDialog(self,"Find...")
        self.textbox.focus_set()
        if findReplaceSettings.go:
            self.doFind()
    
    def findAgain(self,event=None):
        """Repeat find."""
        if findReplaceSettings.search=="":
            self.find()
        else:
            findReplaceSettings.go=True
            self.doFind()

    def doReplace(self,event:Event=None):
        findReplaceSettings.isreplace=True
        try:
            selected=self.textbox.index(SEL_FIRST)
        except:
            selected=False
        findReplaceSettings.selection=bool(selected)
        FindReplaceDialog(self,"Replace...")
        if findReplaceSettings.go:
            self.doFind()
        self.textbox.focus_set()
        return "break"

    def doFind(self,event=None):
        """Perform find command"""
        search=findReplaceSettings.search
        options={"backwards":findReplaceSettings.backward}
        options["nocase"]=not findReplaceSettings.caseSensitive
        if findReplaceSettings.wordmatch:
            options["regexp"]=True
            search=r"\y"+(re.sub(r"([\\^.?*<>\[\]$])",r"\\\1",search))+r"\y"

        replaceall=findReplaceSettings.all and findReplaceSettings.isreplace
        if replaceall:
            if findReplaceSettings.selection:
                start=SEL_FIRST
                end=SEL_LAST
            else:
                start="1.0"
                end=END
        foundonce=False
        while True:
            if replaceall:
                found=self.textbox.search(search,start,end,**options)
            elif findReplaceSettings.backward:
                ix=self.textbox.index(INSERT+" -1 chars")
                found=self.textbox.search(search, ix,"1.0",**options)
                if not(found):
                    found=self.textbox.search(search, END,ix,**options)
            else:            
                ix=self.textbox.index(INSERT)+"+1 chars" 
                found=self.textbox.search(search, ix,END,**options)
                if not(found):
                    found=self.textbox.search(search, "1.0",ix,**options)
            if found:
                foundonce=True
                lx=len(findReplaceSettings.search)
                if findReplaceSettings.isreplace:
                    self.textbox.delete(found,found+("+%d chars" % lx))
                    self.textbox.insert(found,findReplaceSettings.replace)
                    lx=len(findReplaceSettings.replace)
                self.textbox.mark_set(INSERT,found)
                self.textbox.see(found)
                self.textbox.focus_set()
                self.textbox.tag_remove("found","1.0",END)
                self.textbox.tag_add("found",found,found+("+%d chars" % lx))
                self.textbox.tag_configure("found",background="blue",foreground="white")
                self.lastfind=found
                if replaceall:
                    start="%s +%d chars" % (found,lx)
                else:
                    break
            else:
                if not(foundonce):
                    messagebox.showwarning("Search",findReplaceSettings.search+" not found.")
                break

    def testName(self)->str:
        return self.caption.lower().replace("*","").replace("=","_").replace("#","").replace(":","_")
    
    def setcolors(self):
        """Initialize colour tags"""
        for col in self.COLORLIST:
            self.textbox.tag_configure(col,foreground=col)
        self.textbox.tag_configure("bracket",foreground="white",background="red")
        self.textbox.tag_raise(SEL) # Selection should have priority.

    def lastLine(self)->int:
        """Highest line no of edit"""
        return int(self.textbox.index("end").split(".")[0])

    def getLine(self,lno:int)->str:
        """Return a selected line number."""
        return self.textbox.get(str(lno)+".0",str(lno)+".end")
    
    def cleartags(self,lno:int)->None:
        """Remove tags from a line"""
        for tag in self.COLORLIST:
            self.textbox.tag_remove(tag,str(lno)+".0",str(lno)+".end")
    
    def cleartagRegion(self,startno,endno:int):
        """Remove tags from multiple lines"""
        for tag in self.COLORLIST:
            self.textbox.tag_remove(tag,str(startno)+".0",str(endno)+".end")
    
    def highlight(self,clear:bool=False):
        """Syntax highlight all visible lines"""
        topline=int(self.textbox.index("@0,0").split(".")[0])
        bottomline=int(self.textbox.index("@0,%d" % self.textbox.winfo_height()).split(".")[0])
        if clear:
            self.cleartagRegion(topline,bottomline)
            self.syntaxlist.clear()
            self.textbox.edit_modified(False)
        for i in range(topline,bottomline+1):
            if not(i in self.syntaxlist):
                self.syntaxHighlight(i,False)
                self.syntaxlist.add(i)
        self.trackLocation()

    def syntaxHighlight(self, lno:int, clearline:bool=True):
        line=""
        x:int=0
        
        def nextWord()->str:
            nonlocal x
            result=''
            while x<len(line):
                c=line[x]
                if c in ' "()[]+-/\\*:.\{\}': 
                    if result=="":
                        result=c
                        x+=1
                    return result
                result+=c
                x+=1
            return result
        
        if (lno>=self.lastLine()) or (lno<1):
              return
        if clearline:              
            self.cleartags(lno)
        if not(self.syntax): return
        if lno==0 and self.mode==self.MODE_CODE: return # Leave programming line alone.
        line=self.getLine(lno)

        isquote=False
        isescaped=False
        isverb=False
        isproperty=True
        wordonly=False
        x=0
        color="white"
        nextcolor="white"
        while (x<len(line)-1):
            startx=x
            myword=nextWord()
            if (isescaped):
                isescaped=False
            elif isquote:
                color="yellow"
                if myword=="\\":
                    isescaped=True
                    color="orange"
                elif myword=='"':
                    isquote=False
                    wordonly=True
            elif (myword=='"'):
                isquote=True;
                color="yellow"
            else:
                if myword==':': nextcolor="magenta"
                elif myword=='.': nextcolor="lawn green"
                elif (nextcolor!="white"):
                    color=nextcolor
                    nextcolor="white"
                    wordonly=True
                elif myword.lower() in self.KEYWORDLIST: 
                    color="cyan"
                    wordonly=True
            self.setSynColor(color,lno,startx,x)
            if wordonly:
                color="white"
            wordonly=False
    
    def setSynColor(self,color:str, lno:int, start:int, end:int)->None:
        fromix="%d.%d" % (lno,start)
        toix="%d.%d" % (lno,end)
        self.textbox.tag_add(color,fromix,toix)

if __name__=="__main__":
    root=Tk()
    root.title("Test Code Editor")
    c=CodeText(root,CodeText.MODE_CODE, background="black",foreground="white",font=("Courier",12,"bold"),insertbackground="white", nowrap=True)
    c.pack(fill=BOTH,expand=True)
    c.syntax=True
#    c.setLabel("Testing label")
    with open("c:/kev/test.moo","r") as f:
        data=f.read();
        c.setText(data)
    root.mainloop()


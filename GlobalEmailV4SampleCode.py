import json
#Check for Python2.x or Python3.x
try:
    # Python 2.x
    from Tkinter import *
    import ttk
    print("python2.x")
    from urllib2 import urlopen, quote
except ImportError:
    # Python 3.x
    from tkinter import *
    from tkinter import ttk
    from urllib.request import urlopen, quote
    
    print("python3.x")

#========================================#
#GUI Class for Global Email V4
#========================================#
class GlobalEmailV4(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.checkCmd = IntVar()
        self.initUI()

    #========================================#
    #GUI creator
    #========================================#
    def initUI(self):
        self.master.title("Global Email V4")
        
        #Left and Right Frames
        lFrame = Frame(self.master, bg= "#ededed",width = 300, height = 600, relief = SUNKEN)
        rFrame = Frame(self.master, bg= "white",width = 500, height = 600)
        lFrame.pack(side = LEFT, anchor = NW, expand=YES, fill = X,pady=100)
        rFrame.pack(side = RIGHT)     

        #Create Notebook Tabs
        nb = ttk.Notebook(rFrame,width = 500, height = 600)
        nb.grid(row=0, column = 0, columnspan=500,rowspan=500, sticky= 'NESW')
        tabRequest = ttk.Frame(nb)
        nb.add(tabRequest, text='Request')
        tabResponse = ttk.Frame(nb)
        nb.add(tabResponse, text='Response')

        #Input Values (License and Email)
        inputFrame = Frame(lFrame,bd = 2)
        
        lblLicense = Label(inputFrame,text = "License String")
        lblLicense.pack()

        self.txtLicense = Entry(inputFrame,width = 30)
        self.txtLicense.insert(END,"DEMO")
        self.txtLicense.pack()

        lblEmail = Label(inputFrame,text= "Email")
        lblEmail.pack()

        self.txtEmail = Entry(inputFrame,width = 30)
        self.txtEmail.insert(END,"test@domain.com")
        self.txtEmail.pack()
        inputFrame.pack(pady=20)

        #Check Boxes (Domain Correction)
        dcFrame = Frame(lFrame,bd = 2)
        self.chkDomainCorrect = Checkbutton(dcFrame, onvalue = 1, offvalue = 0, variable = self.checkCmd)
        self.chkDomainCorrect.select()
        self.chkDomainCorrect.pack(side = RIGHT, anchor = W,padx = 5)
        lblDomainCorrect = Label(dcFrame,text = "Domain Correction")
        lblDomainCorrect.pack(side = RIGHT, anchor = W,padx = 5)
        dcFrame.pack(expand = 1, padx = 20, pady = 5)
        
        
        #Combo Boxes (WhoIs, Verification, TTW)
        cmbFrame = Frame(lFrame,bd = 2)
        
        lblWhoIs = Label(cmbFrame,text = "WhoIs Lookup Domain")
        lblWhoIs.pack()

        self.cmbWhoIs = ttk.Combobox(cmbFrame,values = ["On","Off"])
        self.cmbWhoIs.current(0)
        self.cmbWhoIs.pack()

        lblDomainCorrection = Label(cmbFrame,text = "Domain Correct")
        lblDomainCorrection.pack

        lblMode = Label(cmbFrame,text = "Verification Mode")
        lblMode.pack()

        self.cmbMode = ttk.Combobox(cmbFrame,values = ["Express","Premium"])
        self.cmbMode.current(0)
        self.cmbMode.pack()
        
        lblTTW = Label(cmbFrame,text = "Time to Wait")
        lblTTW.pack()
    
        ttwList = []
        for num in range (5,46):
            ttwList.append(num)
                           
        self.cmbTTW = ttk.Combobox(cmbFrame,values = ttwList)
        self.cmbTTW.current(0)
        self.cmbTTW.pack()

        cmbFrame.pack(pady=20)

        self.txtBRequest = Text(tabRequest, height = 300, width = 500)
        self.txtBRequest.pack()

        self.txtBResponse = Text(tabResponse, height = 300, width = 500)
        self.txtBResponse.pack()

        #BUTTONS (submit, clear)
        bFrame = Frame(lFrame,bd = 1)
        
        btnClear = Button(bFrame,text = "Clear", command = self.clearAll)
        btnClear.pack(side = RIGHT, anchor = W,padx = 5)

        btnSubmit = Button(bFrame,text = "Submit",command = self.Submit)
        btnSubmit.pack(side = RIGHT, anchor = W, padx = 5)

        bFrame.pack(expand = 1, padx = 20, pady = 20)
        
    #========================================#
    #Clear All
    #========================================#
    def clearAll(self):
        self.txtEmail.delete(0,'end')
        self.txtLicense.delete(0,'end')

        self.clearResults()
        
    def clearResults(self):
        self.txtBRequest.delete('1.0',END)
        self.txtBResponse.delete('1.0',END)
        
    #========================================#
    #Submit
    #========================================#
    def Submit(self):
        self.clearResults()

        URL = r"http://globalemail.melissadata.net"
        RESTRequest = ""
        Options = ""

        #================#
        #Inputs
        #================#
        RESTRequest += "&id=" + quote(self.txtLicense.get())
        RESTRequest += "&email=" + quote(self.txtEmail.get())
        
        #================#
        #options
        #================#
        #Domain Correction
        if self.checkCmd.get()  == 0:
            Options+= "DomainCorrection:off,"
            
        #Verify Mailbox
        if self.cmbMode.current() == 1:
            Options+= "VerifyMailbox:Premium,"

        if self.cmbWhoIs.current() == 1:
            Options += "WhoIsLookup:off,"

        #Time to Wait
        Options += "TimeToWait:" +(self.cmbTTW.get())

        #Add options
        RESTRequest += "&opt=" + Options

        #================#
        #Rest Query
        #================#
        format = "json"
        
        RESTRequest = URL + r"/V4/WEB/GlobalEmail/doGlobalEmail?t=" + RESTRequest + "&format="+format
        self.txtBRequest.insert(END,RESTRequest)
        
        retryCounter = 0
        Success = False
        while retryCounter < 5 and not Success:
            try:
                resp = urlopen(RESTRequest)
                jsonResponse = json.loads(resp.read().decode('utf-8'))
                dump = json.dumps(jsonResponse,indent=4,sort_keys=True)
                self.txtBResponse.insert(END,dump)
                print ("Success")
                Success = True
            except:
                retryCounter+=1
                print("Retrying")
    
#========================================#
#Main
#========================================# 
def main():
    root = Tk()
    root.style = ttk.Style()
    root.style.theme_use("alt")
    root.geometry("750x750")
    app = GlobalEmailV4()
    root.mainloop()
        
                          


if __name__ == '__main__':
    main()

import requests, time, multiprocessing, os
from random import choice
from tkinter import filedialog
from tkinter import *

#Loop for each word
def ignSeeker(word_file, startPos = -1, timeOut = 1) :
    #Init counter
    count = 0
    if startPos == "" :
        startPos = 0
    elif type(startPos) == int:
        return
    else :
        pass
    word_array = word_file.readlines()
    start = time.time() #start timer
    # Loop for each word
    for i in enumerate(word_array):
        if i == (startPos + 1) :
            count = i
            for x in range(len(word_array)):
                word = word_array[x].strip()
                response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{(word)}")
                if response.status_code == 204: #204 = untaken
                    print(f"{word} is not claimed (#{count})")
                    unclaimed_file = open("unclaimed.txt", "a")
                    unclaimed_file.write(word + "\n")
                    unclaimed_file.close()
                elif response.status_code == 200: #200 = taken
                    print(f"{word} is already claimed (#{count})")
                    claimed_file = open("claimed.txt", "a")
                    claimed_file.write(word + "\n")
                    claimed_file.close()
                elif response.status_code == 429: #Connection refused
                    time.sleep(600) #10 mins
                    startPos -= 1
                count += 1
                time.sleep(timeOut) #Sleep for 1 sec because of mojang api limitations
            #When done
            end = time.time()
            print(f"Done! ({end-start}) seconds")
            time.sleep(5)



class WindowUI : 
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x300")
        self.root.title("Minecraft IGN Seeker")


        startPosText = Label(self.root, text = "Select the pos you want to start from")
        startPosText.pack()
        startPosEntry = Entry(self.root)   
        startPosEntry.pack()

        v1 = DoubleVar()

        timeoutText = Label(self.root, text = "Time to pause between actions (in seconds)")
        timeoutText.pack()
        timeoutSlider = Scale(self.root, variable = v1, from_ = 0.00, to = 10.00, digits = 3, resolution = 0.1, orient = HORIZONTAL)   
        timeoutSlider.pack()

        buttonGo = Button(self.root, text = "Go!", command = lambda: [self.newIgnSeeker(startPosEntry.get(), v1.get())])
        buttonGo.pack(pady = 5)

        buttonQuit = Button(self.root, text = "Quit!", command = self.root.destroy)
        buttonQuit.pack(pady = 5)

        self.log = Entry(self.root)
        self.log.pack()


        self.root.mainloop()
    
    def newIgnSeeker(self, startPos = 0, timeOut = 0) :
        p = multiprocessing.Process(target = ignSeeker(open(filedialog.askopenfilename(), "r"), startPos, timeOut))
        p.start()
        
        self.log.configure(state = "normal")
        self.log.insert("1.0", f"")
        self.log.configure(state = "disabled")

if __name__ == '__main__' :
    startUI = WindowUI()
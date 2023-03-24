class Main:
    def __init__(self, file: str, startPos: int, timeout = 1):
        #Init counter
        if startPos == "":
            startPos = 0
        count = startPos
        word_file = open(file, "r")
        word_array = []
        for word in word_file:
            if len(word) > 3:
                word_array.append(word.strip())
        word_file.close()
        start = time.time() #start timer
        # Loop for each word
        len_array = len(word_array)
        headers = {'Content-Type': 'application/json'}
        while count < len_array:
            difference = len_array - count
            payload = []
            for i in range(difference if difference < 10 else 10):
                payload.append(word_array[count+i])
            request = requests.post("https://api.mojang.com/profiles/minecraft", headers = headers, data = json.dumps(payload))
            response = request.json()
            if request.status_code == 429:
                count -= difference
                time.sleep(600)
            else:
                len_response = len(response)
                payload_sorted = sorted(payload)
                payload_index = 0
                content_index = 0
                while payload_index < len_response:
                    payload_item = payload_sorted[payload_index]
                    if payload_item != response[content_index]["name"].lower():
                        print(f"{payload_item} is available (#{count+payload_index})")
                        unclaimed_file = open("unclaimed.txt", "a")
                        unclaimed_file.write(payload_item + "\n")
                        unclaimed_file.close()
                        content_index-=1
                    else:
                        print(f"{payload_item} is already used (#{count+payload_index})")
                        claimed_file = open("claimed.txt", "a")
                        claimed_file.write(payload_item + "\n")
                        claimed_file.close()
                    payload_index+=1
                    content_index+=1
            count += 10
            time.sleep(timeout)
        end = time.time()
        print(f"Done! ({end-start} seconds)")
        input()

class WindowUI: 
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
    
    def newIgnSeeker(self, startPos = 1, timeout = 30):
        ignSeeker = Main(filedialog.askopenfilename(), startPos, timeout)
        p = multiprocessing.Process(target = ignSeeker)
        p.start()
        
        self.log.configure(state = "normal")
        self.log.insert(0, f"")
        self.log.configure(state = "disabled")

if __name__ == '__main__':
    import requests, time, multiprocessing, json, sys
    try:
        from tkinter import filedialog
        from tkinter import *
        startUI = WindowUI()
    except:
        print("Program started in nogui mode because no tkinter module was found")
        start = Main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
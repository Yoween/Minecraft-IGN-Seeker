import requests, time
from random import choice
from tkinter import filedialog

#Init counter
count = 0
pos = -1
#Loop for each word
print("Please select the word list file")
with open(filedialog.askopenfilename(), "r") as word_file:
    #Open files and ask for start pos
    word_array = word_file.readlines()
    print("Starting with {0} words.".format(len(word_array)))
    pos = input("Select the pos you want to start from (empty for 0): ")
    if pos == "" or pos == " ":
        pos = -1
    elif int(pos) > len(word_array):
        print("Specified number is bigger than the list itself")
        time.sleep(5)
    elif int(pos) <= len(word_array):
        pos=(int(pos)-1)
    start = time.time() #start timer
    # Loop for each word
    for i, line in enumerate(word_array):
        if i == (pos + 1) :
            count = i
            for x in range(len(word_array)):
                word = word_array[x].strip()
                response = requests.get("https://api.mojang.com/users/profiles/minecraft/{0}".format(word))
                if response.status_code == 204: #204 = untaken
                    print("{0} is not claimed (#".format(word)+ str(count) +")")
                    unclaimed_file = open("_unclaimed.txt", "a")
                    unclaimed_file.write(word + "\n")
                    unclaimed_file.close()
                elif response.status_code == 200: #200 = taken
                    print("{0} is already claimed (#".format(word)+ str(count) +")")
                    claimed_file = open("_claimed.txt", "a")
                    claimed_file.write(word + "\n")
                    claimed_file.close()
                elif response.status_code == 429: #Connection refused
                    time.sleep(600) #10 mins
                    pos -= 1
                count += 1
                time.sleep(1) #Sleep for 1 sec because of mojang api limitations
            #When done
            end = time.time()
            print("Done! ("+str(end-start)+") seconds")
            time.sleep(5)

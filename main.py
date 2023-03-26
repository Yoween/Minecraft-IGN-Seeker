class Main:
    def __init__(self, file: str, startPos: int, timeout = 1):
        self.valid_chars = list(string.ascii_lowercase + string.digits) 
        try:
            if startPos == "":
                startPos = 0
            count = int(startPos)
            word_file = open(file, "r")
            word_array = []
            invalid = False
            for word in word_file:
                word = word.strip()
                word = word.lower()
                if len(word) > 3:
                    if self.is_valid(word):
                        word_array.append(word)
                    else:
                        invalid = True
                else:
                    invalid = True
            if invalid:
                print("Some words are shorter than the minimum allowed by Mojang or contains invalid characters.\nIndexes may not be accurate to the provided list\nBUT WILL BE for the program if you want to change the starting position.")
                if input("Still want to continue? y/n: ") != "y":
                    return
            word_file.close()
            word_array = list(dict.fromkeys(word_array))
            start = time.time()
            len_array = len(word_array)
            headers = {'Content-Type': 'application/json'}
            print(f"Starting with {len_array} words. Press Ctrl + C to cancel at any moment")
            while count < len_array:
                difference = len_array - count
                payload = []
                for i in range(difference if difference < 10 else 10):
                    payload.append(word_array[count+i])
                request = requests.post("https://api.mojang.com/profiles/minecraft", headers = headers, data = json.dumps(payload))
                if request.status_code == 429:
                    print("Timed out due to too many requests. Waiting a bit to go again")
                    time.sleep(30)
                else:
                    response = request.json()
                    payload_sorted = sorted(payload)
                    payload_index = 0
                    content_index = 0
                    while payload_index < len(payload_sorted):
                        payload_item = payload_sorted[payload_index]
                        try:
                            if payload_item != response[content_index]["name"].lower():
                                self.output(0, payload_index, payload_item, count)
                                content_index -= 1
                            else:
                                self.output(1, payload_index, payload_item, count)
                        except:
                            self.output(0, payload_index, payload_item, count)
                            content_index -= 1
                        payload_index += 1
                        content_index += 1
                count += 10
                if count % 100 == 0:
                    print(f"{count} word checked! {len_array - count} left!")
                time.sleep(timeout)
            end = time.time()
            print(f"Done! ({end-start} seconds)")
            input()
        except KeyboardInterrupt as e:
            print(f"Task cancelled due to human interruption. You can start back from where you were at by setting the starting position to {count}")
        except Exception as e:
            print("Unexpected error:", e)
            
    def is_valid(self, word):
        valid = True
        for char in word:
            if char not in self.valid_chars:
                valid = False
        return valid
    
    def output(self, state, index, item, count):
        if state == 0:
            print(u"\u2714 " + f"{item} is available (#{count + index})")
            unclaimed_file = open("unclaimed.txt", "a")
            unclaimed_file.write(item + "\n")
            unclaimed_file.close()
        elif state == 1:
            print(u"\u274c " + f"{item} is already used (#{count + index})")
            claimed_file = open("claimed.txt", "a")
            claimed_file.write(item + "\n")
            claimed_file.close()

if __name__ == '__main__':
    import requests, time, json, sys, string
    len_args = len(sys.argv)
    pos = 0
    pause = 0.5
    if len_args == 1:
        try:
            import tkinter as tk
            from tkinter import filedialog

        except:
            print("No tkinter found. Please start the program by command line")
            
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename()
        start = Main(file, pos, pause)
        exit()
    try:
        if len_args > 1:
            file = sys.argv[1]
        else:
            print("Missing arguments! Please at least input the file you wanna use.")
        if len_args > 2:
            pos = int(sys.argv[2])
        if len_args > 3:
            pause = float(sys.argv[3])
    except ValueError as e:
        print("Please only use integers for the start position!")
        exit()
    except IndexError as e:
        pos = 0
        pause = 1
    except Exception as e:
        print(e)
        exit()
    start = Main(file, pos, pause)
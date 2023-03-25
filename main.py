class Main:
    def __init__(self, file: str, startPos: int, timeout = 1):
        #Init counter
        try:
            if startPos == "":
                startPos = 0
            count = int(startPos)
            word_file = open(file, "r")
            word_array = []
            invalid = False
            for word in word_file:
                if len(word) > 3:
                    word_array.append(word.strip())
                else:
                    invalid = True
            if invalid:
                print("Some words are shorter than the minimum allowed by Mojang.\nIndexes may not be accurate to the provided list\nBUT WILL BE for the program if you want to change the starting position.")
                if input("Still want to continue? y/n: ") != "y":
                    return
            word_file.close()
            start = time.time()
            len_array = len(word_array)
            headers = {'Content-Type': 'application/json'}
            print(f"Starting with {len_array} words")
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
                        except:
                            print(f"{payload_item} is already used (#{count+payload_index})")
                            claimed_file = open("claimed.txt", "a")
                            claimed_file.write(payload_item + "\n")
                            claimed_file.close()
                        payload_index+=1
                        content_index+=1
                count += 10
                if count % 100 == 0:
                    print(f"{count} word checked! {len_array - count} left!")
                time.sleep(timeout)
            end = time.time()
            print(f"Done! ({end-start} seconds)")
            input()
        except Exception as error:
            print("Unexpected error:", error)

if __name__ == '__main__':
    import requests, time, multiprocessing, json, sys
    len_args = len(sys.argv)
    if len_args > 1:
        file = sys.argv[1]
        try:
            pos = int(sys.argv[2])
            pause = float(sys.argv[3])
        except ValueError as e:
            print("Please only use integers for the start position!")
            exit()
        except Exception as e:
            print(e)
            pos = 0
            pause = 1
        start = Main(file, pos, pause)
    else:
        print("Missing arguments! Please at least input the file you wanna use.")
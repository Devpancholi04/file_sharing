import socket as sk
import os 
import time 
import tkinter as tk
from tkinter import filedialog

class fileApp:
    def __init__(self,root):
        self.root = root
        self.root.title("File Transfer App")
        self.root.geometry("500x500")

        self.host = "192.168.1.100"
        self.port = 33875

        self.send_button = tk.Button(root, text = "send", command=self.send, width=20, font = ("",20, "bold"))
        self.send_button.pack(pady = 20)

        self.receive_button = tk.Button(root, text = "receive", command=self.recevier, width=20, font = ("",20, "bold"))
        self.receive_button.pack(pady = 20)

        self.exit_button = tk.Button(root, text = "exit", command=self.exit_but, width=20, font = ("",20, "bold"))
        self.exit_button.pack(pady = 20)
        
    
    def exit_but(self):
        self.root.quit()
        self.root.destroy()


    def send(self):
        file_path = filedialog.askopenfilename()
        print(file_path)

        file_name = os.path.basename(file_path)
        print(f"file name : {file_name}")
        
        file_size = os.path.getsize(file_path)

        if file_size >= 1000 and file_size < 1000000:
            file_new_size = file_size / 1000
            print(f"file_size : {file_new_size} KB")
        elif file_size >= 1000000 and file_size < 1000000000:
            file_new_size = file_size / 1000000
            print(f"file_size : {file_new_size} MB")
        elif file_size >= 1000000000:
            file_new_size = file_size / 1000000000
            print(f"file_size : {file_new_size} GB")
        else:
            print(f"file size : {file_size} bytes")

        s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        s.connect((self.host, self.port))

        try:
            file_info = f"{file_name}:{file_size}:{file_new_size}".encode("utf-8")
            s.sendall(file_info)

            with open(file_path, "rb") as f:
                while True:
                    data = f.read(1024*10000)
                    time.sleep(1)
                    if not data:
                        break
                    s.sendall(data)
            print(f"file {file_name} of {file_new_size} has been send successfully")
        except Exception as e:
            print(f"error : {e}")
        finally:
            s.close()

    def recevier(self):
        s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)

        save_path = filedialog.askdirectory()
        print(save_path)
        

        while True:
            print("waiting for connection......")

            connection, client_address = s.accept()
            try:
                print(f"getting connection from......{client_address}")

                file_info = connection.recv(1024).decode("utf-8").split(":")
                file_name = "Received_" + file_info[0]
                file_size = int(file_info[1])
                file_new_size = file_info[2]

                save_loc = os.path.join(save_path,file_name)

                with open(save_loc, "wb") as f:
                    received_size = 0
                    while received_size < file_size:
                        data = connection.recv(1024*10000)
                        if not data:
                            print("no data")
                            break
                        else:
                            f.write(data)
                            received_size += len(data)
                print(f"file {file_name} of {file_new_size} received successfully.......")             

            except Exception as e:
                print(f"error : {e}")
            finally:
                connection.close()  

if __name__ == "__main__":

    root = tk.Tk()
    app = fileApp(root)
    root.mainloop()
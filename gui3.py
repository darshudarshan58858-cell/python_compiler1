import tkinter as tk

def show_name():
    name = entry.get()
    result_label.config(text=f"Hello, {name}!")
    
 # create the main window
 
root = tk.Tk()
root.title("Name Input")
root.geometry("400x250") 
root.configure(bg="lightblue")

#title 
tk.Label(root, text="Enter Your Name", 
         font=("Arial", 16, "bold"), bg="lightblue").pack(pady=20)  

# entry box
entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=10)         

# submit button

tk.Button (root, text="Submit", command=show_name, bg= "white", fg="black", font=("Arial" , 12), width=10).pack(pady=10)

#result label
result_label = tk.Label(root, text="", font=("Arial", 14), fg= "green", bg="lightblue")
result_label.pack(pady=20)

root.mainloop()
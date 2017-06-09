from tkinter import *
from tkinter.ttk import *
from RSA import *
from tkinter import messagebox

def layout():
	# key layout
	keySize_label.grid(column=0, row=0)
	keySize_box.grid(column=1, row=0)
	getKey_button.grid(column=2, row=0)
	pub_label.grid(row=1, columnspan=2, padx=5, pady=5)
	prv_label.grid(column=2, row=1, columnspan=2, padx=5, pady=5)
	pub_text.grid(column=0, columnspan=2, padx=5, pady=5)
	prv_text.grid(column=2, row=2, columnspan=2)

	# encrypt/decrypt layout
	method_label.grid(column=0, row=3, padx=5, pady=5)
	method_box.grid(column=1, row=3, padx=5, pady=5)
	encrypt_button.grid(column=2, row=3, padx=5, pady=5)
	decrypt_button.grid(column=3, row=3, pady=5)
	p_label.grid(row=4, columnspan=2)
	c_label.grid(column=2, row=4, columnspan=2)
	p_text.grid(column=0, columnspan=2, padx=5, pady=5)
	c_text.grid(column=2, row=5, columnspan=2)

def click_key(rsa):
	pub_text.delete(1.0, END)
	prv_text.delete(1.0, END)
	keysize = keySize_box.get()
	rsa.setKeySize(int(keysize))
	rsa.generate_key()
	pub_text.insert(END, rsa.getPubKey())
	prv_text.insert(END, rsa.getPrvKey())

def click_encrypt(rsa):
	if rsa.p==0:
		messagebox.showerror("Error", "Please generate the key first!") 
	m = p_text.get(1.0, END)
	c = rsa.encrypt(m)
	p_text.delete(1.0, END)
	c_text.delete(1.0, END)
	c_text.insert(END, c)

def click_decrypt(rsa):
	if rsa.p==0:
		messagebox.showerror("Error", "Please generate the key first!") 
	c = c_text.get(1.0, END)
	method = method_box.get()
	m = rsa.decrypt(c, method)
	c_text.delete(1.0, END)
	p_text.delete(1.0, END)
	p_text.insert(END, m)

if __name__ == '__main__':
	# create a test obj
	test = RSA()

	# window settings
	win=Tk()
	win.geometry('600x500')
	win.title("RSA Encrypt/Decrypt")

	# key
	keySize_label = Label(win, text="Key Size (bit):")
	pub_label = Label(win, text="Public Key")
	prv_label = Label(win, text="Private Key")
	pub_text = Text(win, height=10, width=40, highlightbackground="black")
	prv_text = Text(win, height=10, width=40, highlightbackground="black")
	keySize_box = Combobox(win, state='readonly')
	keySize_box['values'] = ('1024', '2048', '4096')
	keySize_box.current(0)
	getKey_button = Button(win, text="Generate Key", command=lambda:click_key(test))

	# encrypt/decrypt
	p_label = Label(win, text="Plaintext")
	c_label = Label(win, text="Ciphertext")
	p_text = Text(win, height=10, width=40, highlightbackground="black")
	c_text = Text(win, height=10, width=40, highlightbackground="black")
	method_label = Label(win, text="Decrypt:")
	method_box = Combobox(win, state='readonly')
	method_box['values'] = ("Square and Multiply", "CRT")
	method_box.current(0)
	encrypt_button = Button(win, text="Encrypt", command=lambda:click_encrypt(test))
	decrypt_button = Button(win, text="Decrypt", command=lambda:click_decrypt(test))
	
	layout()
	win.mainloop()
import tkinter as tk
import sqlite3

"""Payment management system
    Written by Hawkins647"""


root = tk.Tk()
root.title("Payment Management System")
root.geometry("600x600")
root.resizable(0, 0)

inbound_db = sqlite3.connect("inbound.sqlite")
outbound_db = sqlite3.connect("outbound.sqlite")


def delete_entry_inbound(scrollbox):
    """Deletes the selected entry from the inbound_payments database
    PARAMETERS:
         scrollbox: The tkinter Scrollbox widget that is on the main frame."""

    for i in scrollbox.curselection():
        # Split the selection into a list
        value_list = scrollbox.get(i).split()

        # Delete the selection using the name and amount to identify the chosen value
        inbound_db.execute('DELETE FROM inbound_payments WHERE "name"=' + '"' + value_list[1].strip(",") + '"' + ' AND "amount"=' + value_list[3].strip(","))

    # Call the inbound_menu function to refresh the page, updating the deletion
    inbound_menu()


def delete_entry_outbound(scrollbox):
    """Deletes the selected entry from the outbound_payments database
    PARAMETERS:
        scrollbox: The tkinter Scrollbox widget that is on the main frame."""

    for i in scrollbox.curselection():
        # Split the selection into a list
        value_list = scrollbox.get(i).split()

        # Delete the selection using the name to identify the chosen value
        outbound_db.execute('DELETE FROM outbound_payments WHERE "name"=' + '"' + value_list[1].strip(",") + '"' + ' AND "amount"=' + value_list[3].strip(","))

    # Call the inbound_menu function to refresh the page, updating the deletion
    outbound_menu()


def register_new_inbound(name, amount, vat):
    """Registers a new entry in the inbound database
    PARAMETERS:
        name: str - The name of the payer
        amount: int (will be given in str form, but must contain an int) - The amount paid
        vat: str - Whether VAT was used or not"""

    inbound_db.execute("CREATE TABLE IF NOT EXISTS inbound_payments (name TEXT, amount INTEGER, vat TEXT)")

    inbound_db.execute("INSERT INTO inbound_payments (name, amount, vat) VALUES('{}', {}, '{}')".format(name, amount, vat))
    inbound_db.commit()

    inbound_menu()


def register_new_outbound(name, amount, vat):
    """Registers a new entry in the outbound database
    PARAMETERS:
        name: str - The name of the payer
        amount: int (will be given in str form, but must contain an int) - The amount paid
        vat: str - Whether VAT was used or not"""

    outbound_db.execute("CREATE TABLE IF NOT EXISTS outbound_payments (name TEXT, amount INTEGER, vat TEXT)")
    outbound_db.execute("INSERT INTO outbound_payments (name, amount, vat) VALUES('{}', {}, '{}')".format(name, amount, vat))
    outbound_db.commit()

    outbound_menu()


def reset_frame():
    """Reset the frame, in order to reset widgets or refresh a page to update information"""

    global main_frame

    main_frame.destroy()
    main_frame = tk.Frame(root)
    main_frame.pack()


def inbound_menu():
    """Create the inbound payments menu on the main frame"""

    reset_frame()
    title_frame = tk.Frame(main_frame)
    title_frame.grid(row=0, column=0)

    title_label = tk.Label(title_frame, text="Inbound Payments")
    title_label.pack()

    warning_label = tk.Label(main_frame, text="WARNING: PLEASE FILL OUT ALL BOXES TO ENSURE NO ERRORS ARE MADE")
    warning_label.grid(row=1, column=0)

    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=2, column=0)

    tk.Label(button_frame, text="(Company) Name of Payer").grid(row=2, column=0)
    name_entry = tk.Entry(button_frame)
    name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(button_frame, text="Amount of money paid").grid(row=3, column=0)
    amount_entry = tk.Entry(button_frame)
    amount_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(button_frame, text="VAT included? (Y/N)").grid(row=4, column=0)
    vat_entry = tk.Entry(button_frame)
    vat_entry.grid(row=4, column=1, pady=5)

    register_new_button = tk.Button(main_frame, text="Register new payment", command=lambda:register_new_inbound(name_entry.get(), amount_entry.get(), vat_entry.get().upper()))
    register_new_button.grid(row=5, column=0, padx=3, pady=3)

    current_payments_label = tk.Label(main_frame, text="Current Inbound Payments")
    current_payments_label.grid(row=6, column=0, padx=3, pady=20)

    inbound_payments_list = tk.Listbox(main_frame)
    inbound_payments_list.grid(row=7, column=0, sticky='nsew', rowspan=2)
    inbound_payments_list.config(border=2, relief='sunken')

    inbound_db_cursor = inbound_db.cursor()
    inbound_db_cursor.execute("SELECT * FROM inbound_payments")

    for row in inbound_db_cursor:
        inbound_payments_list.insert(tk.END, "Name: " + row[0] + ", Price: " + str(row[1]) + ", VAT: " + row[2])

    listScroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=inbound_payments_list.yview)
    listScroll.grid(row=7, column=1, sticky='nsw', rowspan=2)
    inbound_payments_list['yscrollcommand'] = listScroll.set

    tk.Label(main_frame, text="Please select the entry you want to delete from the options above").grid(row=9, column=0, padx=5, pady=5)

    delete_button = tk.Button(main_frame, text="Delete an entry", command=lambda:delete_entry_inbound(inbound_payments_list), width=20)
    delete_button.grid(row=10, column=0, pady=10)


def outbound_menu():
    """Create the outbound menu on the main frame"""

    reset_frame()
    title_frame = tk.Frame(main_frame)
    title_frame.grid(row=0, column=0)

    title_label = tk.Label(title_frame, text="Outbound Payments")
    title_label.pack()

    warning_label = tk.Label(main_frame, text="WARNING: PLEASE FILL OUT ALL BOXES TO ENSURE NO ERRORS ARE MADE")
    warning_label.grid(row=1, column=0)

    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=2, column=0)

    tk.Label(button_frame, text="(Company) Name of Payee").grid(row=2, column=0)
    name_entry = tk.Entry(button_frame)
    name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(button_frame, text="Amount of money paid").grid(row=3, column=0)
    amount_entry = tk.Entry(button_frame)
    amount_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(button_frame, text="VAT included? (Y/N)").grid(row=4, column=0)
    vat_entry = tk.Entry(button_frame)
    vat_entry.grid(row=4, column=1, pady=5)

    register_new_button = tk.Button(main_frame, text="Register new payment", command=lambda:register_new_outbound(name_entry.get(), amount_entry.get(), vat_entry.get()))
    register_new_button.grid(row=5, column=0, padx=3, pady=3)

    current_payments_label = tk.Label(main_frame, text="Current Inbound Payments")
    current_payments_label.grid(row=6, column=0, padx=3, pady=20)

    outbound_payments_list = tk.Listbox(main_frame)
    outbound_payments_list.grid(row=7, column=0, sticky='nsew', rowspan=2)
    outbound_payments_list.config(border=2, relief='sunken')

    outbound_db_cursor = outbound_db.cursor()
    outbound_db_cursor.execute("SELECT * FROM outbound_payments")

    for row in outbound_db_cursor:
        outbound_payments_list.insert(tk.END, "Name: " + row[0] + ", Price: " + str(row[1]) + ", VAT: " + row[2])

    listScroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=outbound_payments_list.yview)
    listScroll.grid(row=7, column=1, sticky='nsw', rowspan=2)
    outbound_payments_list['yscrollcommand'] = listScroll.set

    tk.Label(main_frame, text="Please select the entry you want to delete from the options above").grid(row=9, column=0, padx=5, pady=5)

    delete_button = tk.Button(main_frame, text="Delete an entry", command=lambda:delete_entry_outbound(outbound_payments_list), width=20)
    delete_button.grid(row=10, column=0, pady=10)


top_button_frame = tk.Frame(root, bg="grey")
top_button_frame.pack(pady=3, fill=tk.BOTH)

main_frame = tk.Frame(root)
main_frame.pack()

inbound_window_button = tk.Button(top_button_frame, text="Inbound Payments", bg="red", width=40, command=inbound_menu)
inbound_window_button.grid(row=0, column=0, padx=3)

outbound_window_button = tk.Button(top_button_frame, text="Outbound Payments", bg="red", width=40, command=outbound_menu)
outbound_window_button.grid(row=0, column=1, padx=3)


root.mainloop()

inbound_db.close()
outbound_db.close()


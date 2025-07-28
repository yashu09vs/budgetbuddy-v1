#library to create ui
import tkinter as tk
#import database functions
from db import connect_db
from db import initialize_db
from db import get_all_expenses

initialize_db() #setup database table if needed


#connect to database and close immediately
conn = connect_db()
print('connection successful') #optional debug can be removed
conn.close()


#creats main application window
window = tk.Tk()
window.title('expense tracker')
window.geometry('500x800') #window size
label = tk.Label(window, text='welcome to the expense tracker', font=('Arial', 16)) #window text
label.pack(pady=20)

#each of these creates a label and an entry box for the information to be input
amountlabel = tk.Label(window, text='amount: ')
amountlabel.pack()

amountentry = tk.Entry(window)
amountentry.pack()

categorylabel = tk.Label(window, text='category: ')
categorylabel.pack()

categoryentry = tk.Entry(window)
categoryentry.pack()

datelabel = tk.Label(window, text='enter date (YYYY-MM-DD): ')
datelabel.pack()

dateentry = tk.Entry(window)
dateentry.pack()

notelabel = tk.Label(window, text='optional notes: ')
notelabel.pack()

noteentry = tk.Entry(window)
noteentry.pack()

#this is to submit the input and write it in the database
def submitexpense():
    amount = float(amountentry.get())
    category = categoryentry.get()
    date = dateentry.get()
    notes = noteentry.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, date, notes)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, date, notes))
    conn.commit()
    conn.close()

    #this is optional and it just clears the input field
    #put to avoid submitting same info twice
    amountentry.delete(0, tk.END)
    categoryentry.delete(0, tk.END)
    dateentry.delete(0, tk.END)
    noteentry.delete(0, tk.END)
    
    refresh_expenseslist()

    print('expense added')

#this refreshes the expense list to retrieve previously uploaded info
def refresh_expenseslist():
    expenses_listbox.delete(0, tk.END)
    expenses = get_all_expenses()
    for expense in expenses:
        expense_id, amount, category, date, notes = expense
        display_text = f"{expense_id}: ${amount:.2f} - {category} ({date})"
        if notes:
            display_text += f' [{notes}]'
        expenses_listbox.insert(tk.END, display_text)



#function to delete an expense added
def delete_expense():
    select_index = expenses_listbox.curselection()
    if not select_index:
        print('no expense selected')
        return
    
    selected_text = expenses_listbox.get(select_index)

    try:
        expense_id = int(selected_text.split(':')[0])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()

        refresh_expenseslist()
        print(f'Deleted expense with ID {expense_id}')
    except Exception as e:
        print('error deleting expense: ', e)

#creates a button to delete an entry
deletebutton = tk.Button(window, text='delete selected expense', command=delete_expense)
deletebutton.pack(pady=5)



#creates the button to submit the entry
submitbutton = tk.Button(window, text='add expense', command=submitexpense)
submitbutton.pack(pady=10)

expenses_listbox = tk.Listbox(window, width=75)
expenses_listbox.pack(pady=20)

refresh_expenseslist()
window.mainloop() #start the tkinter event loop to show the window

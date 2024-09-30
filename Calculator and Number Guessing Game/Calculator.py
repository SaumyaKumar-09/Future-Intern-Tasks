import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self):
        self.current_value = 0
        self.full_expression = ""

    def calculate(self, expression):
        try:
            return eval(expression)
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except:
            raise ValueError("Invalid expression")

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        self.calculator = Calculator()
        master.title("Calculator")

        self.display = tk.Text(master, height=2, width=30, font=('Arial', 14), wrap=tk.NONE)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(master, orient='horizontal', command=self.display.xview)
        self.scrollbar.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.display.configure(xscrollcommand=self.scrollbar.set)

        self.create_buttons()

        # Configure row and column weights
        for i in range(7):  # Assuming 6 rows of buttons + 1 row for display
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columns
            master.grid_columnconfigure(i, weight=1)

    def create_buttons(self):
        button_list = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'C', '+'
        ]
        row = 2
        col = 0
        for button in button_list:
            cmd = lambda x=button: self.click(x)
            tk.Button(self.master, text=button, command=cmd).grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1

        tk.Button(self.master, text="=", command=self.calculate).grid(row=row, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')
        tk.Button(self.master, text="Exit", command=self.master.quit).grid(row=row, column=2, columnspan=2, padx=3, pady=3, sticky='nsew')

    def click(self, key):
        if key == 'C':
            self.clear()
        else:
            self.display.insert(tk.END, key)
            self.adjust_display_size()

    def clear(self):
        self.display.delete('1.0', tk.END)
        self.calculator.current_value = 0
        self.calculator.full_expression = ""
        self.adjust_display_size()

    def calculate(self):
        try:
            expression = self.display.get('1.0', tk.END).strip()
            result = self.calculator.calculate(expression)
            self.display.delete('1.0', tk.END)
            self.display.insert('1.0', str(result))
            self.adjust_display_size()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.clear()

    def adjust_display_size(self):
        content = self.display.get('1.0', tk.END).strip()
        lines = content.count('\n') + 1
        self.display.configure(height=min(lines, 5))  # Cap at 5 lines high
        self.display.see(tk.END)  # Scroll to the end of the content

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk


class SimpleCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Calculator")
        self.geometry("260x320")
        self.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        self._create_widgets()

    def _create_widgets(self):
        # Entry Display
        entry = ttk.Entry(
            self,
            textvariable=self.display_var,
            font=("Arial", 18),
            justify="right",
            state="readonly"
        )
        entry.grid(row=0, column=0, columnspan=4,
                   sticky="nsew", padx=10, pady=10)

        # Button Layout
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for text, row, col in buttons:
            def action(val=text): return self._handle_click(val)
            btn = ttk.Button(self, text=text, command=action)
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Configure equal grid cell sizing
        for r in range(5):
            self.rowconfigure(r, weight=1)
        for c in range(4):
            self.columnconfigure(c, weight=1)

    def _handle_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "=":
            try:
                # Basic evaluation (restricted characters)
                sanitized = "".join(
                    c for c in self.expression if c in "0123456789+-*/.")
                result = str(eval(sanitized))
                self.display_var.set(result)
                self.expression = result
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
        else:
            self.expression += char
            self.display_var.set(self.expression)


if __name__ == "__main__":
    app = SimpleCalculator()
    app.mainloop()

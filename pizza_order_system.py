import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. MENU & PRICING DICTIONARIES (Customized)
# ==========================================
pizza_prices = {
    "Ham and Cheese": 250,
    "Bacon": 230,
    "Pepperoni": 320,
    "Hawaiian": 280,
    "Mushroom": 340
}

size_prices = {
    "Solo (8\")": 10,
    "Regular (10\")": 85,
    "Family (14\")": 150
}

topping_prices = {
    "Hotdogs": 15,
    "Black Olives": 15,
    "Pineapples": 12,
    "Extra Mozzarella": 25
}

# ==========================================
# 2. MAIN WINDOW SETUP (Pizza Hut Red & Dark Theme)
# ==========================================
window = tk.Tk()
window.title("Pizza Hut - Order System")
window.geometry("680x820")
window.resizable(True, True)
window.configure(bg="#1a1a1a")  # Deep charcoal background

# ==========================================
# 3. TKINTER VARIABLES
# ==========================================
pizza_var = tk.StringVar(value="Ham and Cheese")
size_var = tk.StringVar(value="Solo (8\")")
quantity_var = tk.IntVar(value=1)

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

# ==========================================
# 4. HEADER & MAIN ORDER CONTAINER
# ==========================================
title = tk.Label(
    window,
    text="🍕 PIZZA HUT ORDER SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#1a1a1a",
    fg="#ee3124"  # Signature Pizza Hut Red
)
title.pack(pady=18)

order_frame = tk.Frame(
    window,
    bg="#262626",  # Dark card container
    padx=25,
    pady=20,
    highlightbackground="#ee3124",  # Red border
    highlightthickness=2
)
order_frame.pack(padx=30, fill="x")

# ==========================================
# 5. PIZZA FLAVOR (Drop-down Combobox)
# ==========================================
tk.Label(
    order_frame,
    text="1. Choose Your Specialty Pizza:",
    font=("Arial", 13, "bold"),
    bg="#262626",
    fg="#ffc72c"  # Golden yellow heading
).pack(anchor="w")

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Arial", 12)
)
pizza_dropdown.pack(fill="x", pady=(5, 15))

# ==========================================
# 6. SIZE & TOPPINGS (Custom 2-Column Layout)
# ==========================================
options_container = tk.Frame(order_frame, bg="#262626")
options_container.pack(fill="x", pady=5)

# Left Column: Pizza Size (Radio Buttons)
size_frame = tk.Frame(options_container, bg="#262626")
size_frame.grid(row=0, column=0, sticky="nw", padx=(0, 40))

tk.Label(
    size_frame,
    text="2. Select Size:",
    font=("Arial", 13, "bold"),
    bg="#262626",
    fg="#ffc72c"
).pack(anchor="w", pady=(0, 5))

for size, price in size_prices.items():
    tk.Radiobutton(
        size_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 10),
        bg="#262626",
        fg="white",
        selectcolor="#ee3124",
        activebackground="#262626",
        activeforeground="#ffc72c"
    ).pack(anchor="w")

# Right Column: Extra Toppings (Checkboxes)
topping_frame = tk.Frame(options_container, bg="#262626")
topping_frame.grid(row=0, column=1, sticky="nw")

tk.Label(
    topping_frame,
    text="3. Extra Toppings:",
    font=("Arial", 13, "bold"),
    bg="#262626",
    fg="#ffc72c"
).pack(anchor="w", pady=(0, 5))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        topping_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 10),
        bg="#262626",
        fg="white",
        selectcolor="#ee3124",
        activebackground="#262626",
        activeforeground="#ffc72c"
    ).pack(anchor="w")

# ==========================================
# 7. QUANTITY (Spinbox)
# ==========================================
tk.Label(
    order_frame,
    text="4. Quantity (1 - 20):",
    font=("Arial", 13, "bold"),
    bg="#262626",
    fg="#ffc72c"
).pack(anchor="w", pady=(15, 5))

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=20,
    textvariable=quantity_var,
    font=("Arial", 12),
    width=8
)
quantity_spinbox.pack(anchor="w")

# ==========================================
# 8. ORDER CALCULATION & RESET FUNCTIONS
# ==========================================
def calculate_total():
    pizza = pizza_var.get()
    size = size_var.get()

    # Validate quantity (1 to 20)
    try:
        quantity = int(quantity_var.get())
        if quantity < 1 or quantity > 20:
            raise ValueError
    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a valid number of pizzas between 1 and 20."
        )
        return

    # Confirmation pop-up
    confirm = messagebox.askyesno(
        "Confirm Pizza Order",
        f"Place order for {quantity}x {size} {pizza}?"
    )
    if not confirm:
        return

    # Compute prices
    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

    total_per_pizza = pizza_price + size_price + topping_price
    grand_total = total_per_pizza * quantity

    # Unlock receipt box, write text, and lock it again
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "==============================================\n")
    receipt_text.insert(tk.END, "              PIZZA HUT RECEIPT               \n")
    receipt_text.insert(tk.END, "==============================================\n\n")
    receipt_text.insert(tk.END, f"Flavor   : {pizza} (₱{pizza_price})\n")
    receipt_text.insert(tk.END, f"Size     : {size} (+₱{size_price})\n")
    receipt_text.insert(tk.END, f"Quantity : {quantity}\n")
    receipt_text.insert(tk.END, "----------------------------------------------\n")
    receipt_text.insert(tk.END, "Extra Toppings:\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(tk.END, f"  + {topping} (₱{topping_prices[topping]})\n")
    else:
        receipt_text.insert(tk.END, "  None\n")

    receipt_text.insert(tk.END, "----------------------------------------------\n")
    receipt_text.insert(tk.END, f"Price per Pizza : ₱{total_per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT    : ₱{grand_total:,.2f}\n")
    receipt_text.insert(tk.END, "==============================================\n")
    receipt_text.config(state="disabled")


def reset_order():
    pizza_var.set("Ham and Cheese")
    size_var.set("Solo (8\")")
    quantity_var.set(1)

    for variable in topping_vars.values():
        variable.set(False)

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.config(state="disabled")

# ==========================================
# 9. ACTION BUTTONS & RECEIPT DISPLAY
# ==========================================
button_frame = tk.Frame(window, bg="#1a1a1a")
button_frame.pack(pady=15)

calculate_button = tk.Button(
    button_frame,
    text="CONFIRM & PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg="#ee3124",  # Signature Pizza Hut Red
    fg="white",
    activebackground="#c82318",
    activeforeground="white",
    width=22,
    command=calculate_total
)
calculate_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(
    button_frame,
    text="RESET ORDER",
    font=("Arial", 11, "bold"),
    bg="#404040",
    fg="white",
    activebackground="#595959",
    activeforeground="white",
    width=14,
    command=reset_order
)
reset_button.grid(row=0, column=1, padx=10)

tk.Label(
    window,
    text="CUSTOMER RECEIPT",
    font=("Arial", 13, "bold"),
    bg="#1a1a1a",
    fg="#ee3124"
).pack(pady=(5, 2))

receipt_text = tk.Text(
    window,
    height=13,
    width=56,
    font=("Consolas", 11),
    bg="#ffffff",  # Crisp white paper receipt
    fg="#1a1a1a",  # Dark ink text
    state="disabled"
)
receipt_text.pack(padx=30, pady=8)

# ==========================================
# 10. RUN APPLICATION
# ==========================================
window.mainloop()

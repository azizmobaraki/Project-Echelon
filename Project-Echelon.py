import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def to_echelon(matrix):
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape
    
    for i in range(rows):
        if i < cols and matrix[i, i] == 0:
            for j in range(i + 1, rows):
                if matrix[j, i] != 0:
                    matrix[[i, j]] = matrix[[j, i]]
                    break
        
        if matrix[i, i] != 0:
            matrix[i] = matrix[i] / matrix[i, i]
            for j in range(i + 1, rows):
                if matrix[j, i] != 0:
                    matrix[j] -= matrix[j, i] * matrix[i]
    
    return matrix

def to_reduced_echelon(matrix):
    matrix = to_echelon(matrix)
    rows, cols = matrix.shape
    
    for i in range(rows - 1, -1, -1):
        for j in range(cols):
            if matrix[i, j] == 1:
                for k in range(i):
                    matrix[k] -= matrix[k, j] * matrix[i]
                break
    
    return matrix

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        return [list(map(float, line.split())) for line in file.readlines()]

def load_matrix():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            matrix = read_matrix_from_file(filename)
            rows, cols = len(matrix), len(matrix[0])
            rows_entry.delete(0, tk.END)
            cols_entry.delete(0, tk.END)
            rows_entry.insert(0, str(rows))
            cols_entry.insert(0, str(cols))
            create_matrix_entries()
            for i in range(rows):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, ' '.join(map(str, matrix[i])))
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خواندن فایل: {e}")
def validate_entry(entry, cols):
    if len(entry.get().split()) != cols:
        entry.configure(style='Error.TEntry')
    else:
        entry.configure(style='TEntry')

def calculate_echelon():
    try:
        rows, cols = int(rows_entry.get()), int(cols_entry.get())
        if rows <= 0 or cols <= 0:
            raise ValueError("تعداد سطرها و ستون‌ها باید بزرگتر از صفر باشند.")
        
        matrix = [list(map(float, entries[i].get().split())) for i in range(rows)]
        echelon_matrix = to_echelon(matrix)
        rank_echelon = calculate_rank(echelon_matrix)
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, str(echelon_matrix))
        result_text.insert(tk.END, f"\nرتبه فرم اشلون: {rank_echelon}\n")
        
    except Exception as e:
        messagebox.showerror("خطا", str(e))

def calculate_reduced_echelon():
    try:
        rows, cols = int(rows_entry.get()), int(cols_entry.get())
        if rows <= 0 or cols <= 0:
            raise ValueError("تعداد سطرها و ستون‌ها باید بزرگتر از صفر باشند.")
        
        matrix = [list(map(float, entries[i].get().split())) for i in range(rows)]
        reduced_echelon_matrix = to_reduced_echelon(matrix)
        rank_reduced_echelon = calculate_rank(reduced_echelon_matrix)
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, str(reduced_echelon_matrix))
        result_text.insert(tk.END, f"\nرتبه فرم اشلون کاهش‌یافته: {rank_reduced_echelon}\n")
        
    except Exception as e:
        messagebox.showerror("خطا", str(e))

def calculate_rank(matrix):
    reduced_matrix = to_reduced_echelon(matrix)
    rank = np.sum(np.any(reduced_matrix != 0, axis=1))
    return rank

def solve_system(matrix):
    rows, cols = matrix.shape
    A = matrix[:, :-1]
    b = matrix[:, -1]
    return np.linalg.solve(A, b)

def check_compatibility():
    try:
        rows, cols = int(rows_entry.get()), int(cols_entry.get())
        if rows <= 0 or cols <= 0:
            raise ValueError("تعداد سطرها و ستون‌ها باید بزرگتر از صفر باشند.")
        
        matrix = [list(map(float, entries[i].get().split())) for i in range(rows)]
        aug_matrix = np.array(matrix)
        coef_matrix = aug_matrix[:, :-1]
        rank_coef = calculate_rank(coef_matrix)
        rank_aug = calculate_rank(aug_matrix)
        
        result_text.delete("1.0", tk.END)
        
        result_text.insert(tk.END, f"رتبه ماتریس ضرایب: {rank_coef}\n")
        result_text.insert(tk.END, f"رتبه ماتریس افزوده: {rank_aug}\n")
        
        if rank_coef == rank_aug:
            if rank_coef == coef_matrix.shape[1]:
                result_text.insert(tk.END, "سیستم سازگار است و دارای یک جواب یکتا است.\n")
                solutions = solve_system(aug_matrix)
                result_text.insert(tk.END, f"جواب‌ها: {solutions}\n")
            else:
                result_text.insert(tk.END, "سیستم سازگار است و دارای بی‌نهایت جواب است.\n")
        else:
            result_text.insert(tk.END, "سیستم ناسازگار است و هیچ جوابی ندارد.\n")
        
    except Exception as e:
        messagebox.showerror("خطا", str(e))

def show_help():
    help_text = (
        "بسم الله الرحمن الرحیم\n"
        "برای استفاده از این برنامه:\n"
        "1. تعداد سطرها و ستون‌های ماتریس را وارد کنید یا یک فایل متنی بارگذاری کنید.\n"
        "2. روی دکمه 'ایجاد ورودی ماتریس' کلیک کنید تا ورودی‌های مربوط به ماتریس ظاهر شوند.\n"
        "3. عناصر هر سطر را با استفاده از فاصله از هم جدا کرده و در ورودی‌های مربوطه وارد کنید یا از فایل بارگذاری شده استفاده کنید.\n"
        "4. پس از وارد کردن تمامی عناصر، می‌توانید با استفاده از دکمه‌های 'محاسبه فرم اشلون' و 'محاسبه فرم اشلون کاهش‌یافته'، نتیجه را مشاهده کنید.\n"
        "5. برای بررسی سازگاری سیستم و نمایش جواب‌ها، از دکمه 'بررسی سازگاری' استفاده کنید."
    )
    messagebox.showinfo("راهنما", help_text)

root = tk.Tk()
root.title("تبدیل ماتریس به فرم اشلون")
root.configure(bg='light blue')

style = ttk.Style()
style.configure('TFrame', background='light blue')
style.configure('TLabel', background='light blue', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TEntry', font=('Helvetica', 12))
style.configure('Error.TEntry', font=('Helvetica', 12), foreground='red')

main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="تعداد سطرهای ماتریس:", style='TLabel').grid(row=0, column=0, pady=5)
rows_entry = ttk.Entry(main_frame, style='TEntry')
rows_entry.grid(row=0, column=1, pady=5)

ttk.Label(main_frame, text="تعداد ستون‌های ماتریس:", style='TLabel').grid(row=1, column=0, pady=5)
cols_entry = ttk.Entry(main_frame, style='TEntry')
cols_entry.grid(row=1, column=1, pady=5)

entries = []
def create_matrix_entries():
    try:
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        entries.clear()
        
        rows, cols = int(rows_entry.get()), int(cols_entry.get())
        
        for i in range(rows):
            ttk.Label(matrix_frame, text=f"سطر {i + 1}:", style='TLabel').grid(row=i, column=0, pady=5)
            entry = ttk.Entry(matrix_frame, width=50, style='TEntry')
            entry.grid(row=i, column=1, pady=5)
            entry.bind("<FocusOut>", lambda event, e=entry, c=cols: validate_entry(e, c))
            entries.append(entry)
    
    except Exception as e:
        messagebox.showerror("خطا", str(e))

matrix_frame = ttk.Frame(main_frame, padding="10 10 10 10", style='TFrame')
matrix_frame.grid(row=2, column=0, columnspan=2)

ttk.Button(main_frame, text="ایجاد ورودی ماتریس", command=create_matrix_entries, style='TButton').grid(row=3, column=0, columnspan=2, pady=5)
ttk.Button(main_frame, text="بارگذاری فایل ماتریس", command=load_matrix, style='TButton').grid(row=4, column=0, columnspan=2, pady=5)
ttk.Button(main_frame, text="محاسبه فرم اشلون", command=calculate_echelon, style='TButton').grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(main_frame, text="محاسبه فرم اشلون کاهش‌یافته", command=calculate_reduced_echelon, style='TButton').grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(main_frame, text="بررسی سازگاری", command=check_compatibility, style='TButton').grid(row=7, column=0, columnspan=2, pady=5)
ttk.Button(main_frame, text="راهنما", command=show_help, style='TButton').grid(row=8, column=0, columnspan=2, pady=5)

ttk.Label(main_frame, text="نتیجه:", style='TLabel').grid(row=9, column=0, pady=5)
result_text = tk.Text(main_frame, height=10, width=50, font=('Helvetica', 12))
result_text.grid(row=10, column=0, columnspan=2, pady=5)

root.mainloop()
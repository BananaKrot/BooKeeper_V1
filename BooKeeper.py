import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

DATA_FILE = "BooKeeper_data.json"

class ReadingDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("BooKeeper")
        self.root.geometry("1920x1080")
        self.root.minsize(800, 500)

        self.books = []
        self.load_data()

        self.current_index = None

        self.create_widgets()
        self.update_book_list()
        self.bind_shortcuts()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except:
                self.books = []
        else:
            self.books = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.books:
            status = "->" if book.get("status") == "Прочитана" else "book"
            display = f"{status} {book['title']} — {book['author']}"
            self.book_listbox.insert(tk.END, display)

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        self.status_combo.set("Читаю")
        self.rating_combo.set("")
        self.notes_text.delete("1.0", tk.END)
        self.date_start_entry.delete(0, tk.END)
        self.date_end_entry.delete(0, tk.END)
        self.current_index = None

    def load_book_to_form(self):
        if self.current_index is None:
            return
        book = self.books[self.current_index]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, book.get("title", ""))
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, book.get("author", ""))
        self.genre_entry.delete(0, tk.END)
        self.genre_entry.insert(0, book.get("genre", ""))
        self.pages_entry.delete(0, tk.END)
        self.pages_entry.insert(0, book.get("pages", ""))
        self.status_combo.set(book.get("status", "Читаю"))
        self.rating_combo.set(book.get("rating", ""))
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", book.get("notes", ""))
        self.date_start_entry.delete(0, tk.END)
        self.date_start_entry.insert(0, book.get("date_start", ""))
        self.date_end_entry.delete(0, tk.END)
        self.date_end_entry.insert(0, book.get("date_end", ""))

    def save_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        if not title or not author:
            messagebox.showwarning("Ошибка", "Название и автор обязательны!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": self.genre_entry.get().strip(),
            "pages": self.pages_entry.get().strip(),
            "status": self.status_combo.get(),
            "rating": self.rating_combo.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "date_start": self.date_start_entry.get().strip(),
            "date_end": self.date_end_entry.get().strip(),
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.current_index is not None:

            self.books[self.current_index] = book
        else:

            self.books.append(book)

        self.save_data()
        self.update_book_list()
        self.clear_fields()
        messagebox.showinfo("Успех", "Книга сохранена!")

    def delete_book(self):
        if self.current_index is None:
            messagebox.showwarning("Ошибка", "Выберите книгу из списка")
            return
        confirm = messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить эту запись?")
        if confirm:
            del self.books[self.current_index]
            self.save_data()
            self.update_book_list()
            self.clear_fields()
            self.current_index = None

    def on_book_select(self, event):
        selection = self.book_listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.load_book_to_form()

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.clear_fields())
        self.root.bind("<Control-s>", lambda e: self.save_book())
        self.root.bind("<Delete>", lambda e: self.delete_book())
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(main_frame, text="Мои книги", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        scrollbar = ttk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_listbox = tk.Listbox(left_frame, yscrollcommand=scrollbar.set,
                                       font=("Segoe UI", 10), height=20)
        self.book_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.book_listbox.yview)
        self.book_listbox.bind("<<ListboxSelect>>", self.on_book_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Новая", command=self.clear_fields).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_book).pack(side=tk.LEFT, padx=2)

        right_frame = ttk.LabelFrame(main_frame, text=" Информация о книге", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        row = 0
        ttk.Label(right_frame, text="Название:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(right_frame, width=40)
        self.title_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Автор:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.author_entry = ttk.Entry(right_frame, width=40)
        self.author_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Жанр").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.genre_entry = ttk.Entry(right_frame, width=40)
        self.genre_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Страницы").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.pages_entry = ttk.Entry(right_frame, width=40)
        self.pages_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Статус").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.status_combo = ttk.Combobox(right_frame, values=["Читаю", "Прочитана", "Брошена"], width=37)
        self.status_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.status_combo.set("Читаю")
        row += 1

        ttk.Label(right_frame, text="Оценка").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.rating_combo = ttk.Combobox(right_frame, values=["", "1", "2", "3", "4", "5"], width=37)
        self.rating_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Дата начала").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.date_start_entry = ttk.Entry(right_frame, width=40)
        self.date_start_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Дата окончания").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.date_end_entry = ttk.Entry(right_frame, width=40)
        self.date_end_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        ttk.Label(right_frame, text="Отзыв").grid(row=row, column=0, sticky=tk.NW, pady=5)
        self.notes_text = scrolledtext.ScrolledText(right_frame, width=50, height=10, wrap=tk.WORD)
        self.notes_text.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
        row += 1

        action_frame = ttk.Frame(right_frame)
        action_frame.grid(row=row, column=0, columnspan=3, pady=15)
        ttk.Button(action_frame, text="Сохранить сtrl+s", command=self.save_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Очистить сtrl+n", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        status_bar = ttk.Label(self.root, text="Горячие клавиши: ctrl+s — сохранить, ctrl+n — новая, delete — удалить", 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReadingDiary(root)
    root.mainloop()
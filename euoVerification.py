import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os
import sys

class LocalDataReviewApp:
    def __init__(self, root, csv_path, img_folder):
        self.root = root
        self.root.title("Form Verifier - Full Integrated Version")
        
        try:
            self.root.state('zoomed') 
        except:
            try: self.root.attributes('-zoomed', True) 
            except: self.root.geometry("1600x1000")

        self.CROP_CONFIG = {
            0: (30, 679, 1652, 154),
            1: (51, 968, 1168, 128),
            2: (30, 1117-40, 2435, 267+40),
        }

        self.csv_path = csv_path
        self.img_folder = img_folder
        self.output_path = csv_path.replace(".csv", "_updated.csv")
        
        self.working_file = self.output_path if os.path.exists(self.output_path) else self.csv_path

        try:
            self.df = pd.read_csv(self.working_file)
            self.df.columns = self.df.columns.str.strip()
            self.ensure_columns()
            
            raw_list = self.df['Cleaned Facility Name'].dropna().unique().tolist()
            self.facility_suggestions = sorted([str(f).strip() for f in raw_list if str(f).strip()])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
            sys.exit()

        self.current_index = self.find_resume_point()
        
        self.setup_ui()
        self.load_row()

    def ensure_columns(self):
        """Prepares the dataframe with necessary tracking columns."""
        required = ["Verified Facility Name", "Verified Date", "Verified Occurrences", "Flagged"]
        for col in required:
            if col not in self.df.columns: self.df[col] = ""
        
        for col in ["Cleaned Facility Name", "Cleaned Date", "Cleaned Occurrences"] + required:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna("")

    def find_resume_point(self):
        """Finds the first row where verified is empty and it hasn't been flagged."""
        try:
            v_name = self.df["Verified Facility Name"].astype(str).str.strip()
            f_stat = self.df["Flagged"].astype(str).str.strip()
            
            unfinished = self.df[(v_name == "") & (f_stat != "YES")]
            return unfinished.index[0] if not unfinished.empty else 0
        except:
            return 0

    def on_facility_type(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return

        typed_text = event.widget.get("1.0", "end-1c").strip()
        if not typed_text:
            self.hide_suggestions()
            return

        matches = [f for f in self.facility_suggestions if typed_text.lower() in f.lower()]
        
        if matches:
            self.suggestion_listbox.delete(0, tk.END)
            for item in matches[:15]:
                self.suggestion_listbox.insert(tk.END, item)
            self.suggestion_frame.place(x=780, y=180) 
            self.suggestion_frame.lift()
        else:
            self.hide_suggestions()

    def select_suggestion(self, event=None):
        if not self.suggestion_listbox.curselection():
            if self.suggestion_listbox.size() > 0:
                self.suggestion_listbox.selection_set(0)
        
        if self.suggestion_listbox.curselection():
            selected = self.suggestion_listbox.get(self.suggestion_listbox.curselection()[0])
            w = self.widgets[0]['entry']
            w.delete("1.0", tk.END)
            w.insert("1.0", selected)
            self.hide_suggestions()
            w.focus_set()
        return "break"

    def handle_suggestion_keys(self, event):
        if not self.suggestion_frame.winfo_viewable(): return
        if event.keysym == "Down":
            self.suggestion_listbox.focus_set()
            if self.suggestion_listbox.size() > 0: self.suggestion_listbox.selection_set(0)
            return "break"
        elif event.keysym == "Escape":
            self.hide_suggestions()
            return "break"

    def hide_suggestions(self):
        self.suggestion_frame.place_forget()

    def open_full_image(self):
        row = self.df.iloc[self.current_index]
        img_path = os.path.join(self.img_folder, f"{row['Report ID']}.png")
        if not os.path.exists(img_path): img_path = img_path.replace(".png", ".jpg")
        if not os.path.exists(img_path): return

        full_img = Image.open(img_path)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        full_img.thumbnail((int(sw*0.9), int(sh*0.9)), Image.Resampling.LANCZOS)
        
        view_win = tk.Toplevel(self.root)
        view_win.title(f"Full View: {row['Report ID']}")
        tk_full = ImageTk.PhotoImage(full_img)
        lbl = tk.Label(view_win, image=tk_full)
        lbl.image = tk_full
        lbl.pack()

    def setup_ui(self):
        top_bar = tk.Frame(self.root, pady=10, bg="#e1e1e1")
        top_bar.pack(fill=tk.X)
        
        tk.Label(top_bar, text="Jump to Index:", bg="#e1e1e1", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        self.row_entry = tk.Entry(top_bar, width=8, font=("Arial", 12))
        self.row_entry.pack(side=tk.LEFT)
        self.row_entry.bind('<Return>', lambda e: self.jump_to_row())
        
        tk.Button(top_bar, text="🔍 VIEW FULL FORM", bg="#555", fg="white", command=self.open_full_image).pack(side=tk.LEFT, padx=20)
        
        self.lbl_status = tk.Label(top_bar, text="Row: 0 / 0", font=("Arial", 14, "bold"), bg="#e1e1e1")
        self.lbl_status.pack(side=tk.RIGHT, padx=30)

        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10)
        main_frame.columnconfigure(0, weight=1)

        self.col_meta = [
            {"title": "Facility Name", "src": "Cleaned Facility Name", "dest": "Verified Facility Name"},
            {"title": "Date (mm/dd/yyyy)", "src": "Cleaned Date", "dest": "Verified Date"},
            {"title": "Occurrences (Use semicolons)", "src": "Cleaned Occurrences", "dest": "Verified Occurrences"},
        ]
        
        self.widgets = []
        for i, meta in enumerate(self.col_meta):
            pane = tk.Frame(main_frame, bd=1, relief=tk.GROOVE)
            pane.grid(row=i, column=0, sticky="nsew", pady=5)
            main_frame.rowconfigure(i, weight=1)

            f_left = tk.Frame(pane, bg="#222", width=750)
            f_left.pack(side=tk.LEFT, fill=tk.BOTH); f_left.pack_propagate(False)
            img_lbl = tk.Label(f_left, bg="#222")
            img_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            f_right = tk.Frame(pane, bg="#f9f9f9")
            f_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=5)
            
            tk.Label(f_right, text=meta['title'], font=("Arial", 16, "bold"), bg="#f9f9f9").pack(anchor="w")
            tk.Label(f_right, text="System Read:", fg="#777", bg="#f9f9f9").pack(anchor="w")
            c_txt = tk.Text(f_right, height=2, font=("Arial", 12), bg="#eee", state=tk.DISABLED); c_txt.pack(fill=tk.X)
            tk.Label(f_right, text="Correction:", bg="#f9f9f9").pack(anchor="w")
            e_txt = tk.Text(f_right, height=3, font=("Arial", 16), wrap=tk.WORD); e_txt.pack(fill=tk.X)
            
            e_txt.bind("<Tab>", self.handle_tab)
            e_txt.bind("<Shift-Tab>", self.handle_shift_tab)
            e_txt.bind('<Return>', lambda e: self.save_and_next_event(e))
            
            e_txt.bind('<Shift-Return>', self.go_back)
            
            if i == 0:
                e_txt.bind("<KeyRelease>", self.on_facility_type)
                e_txt.bind("<KeyPress>", self.handle_suggestion_keys)

            self.widgets.append({"img": img_lbl, "clean": c_txt, "entry": e_txt})

        self.suggestion_frame = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.suggestion_listbox = tk.Listbox(self.suggestion_frame, font=("Arial", 14), width=50, height=8)
        self.suggestion_listbox.pack()
        self.suggestion_listbox.bind("<Double-Button-1>", self.select_suggestion)
        self.suggestion_listbox.bind("<Return>", self.select_suggestion)

        bottom = tk.Frame(self.root, pady=10, bg="#ddd")
        bottom.pack(fill=tk.X)
        self.flag_var = tk.BooleanVar()
        tk.Checkbutton(bottom, text="Flag Record", variable=self.flag_var, font=("Arial", 14), bg="#ddd").pack(side=tk.LEFT, padx=30)
        tk.Button(bottom, text="SAVE & NEXT", bg="#008CBA", fg="white", font=("Arial", 18, "bold"), padx=40, command=self.save_and_next).pack(side=tk.RIGHT, padx=30)
        
        self.root.bind('<Shift-Return>', self.go_back)
        self.root.bind('<Return>', lambda e: self.save_and_next_event(e))

    def load_row(self):
        self.hide_suggestions()
        if not (0 <= self.current_index < len(self.df)): return
        row = self.df.iloc[self.current_index]
        self.lbl_status.config(text=f"Index: {self.current_index} | {row['Report ID']}")
        
        img_path = os.path.join(self.img_folder, f"{row['Report ID']}.png")
        if not os.path.exists(img_path): img_path = img_path.replace(".png", ".jpg")
        base_img = Image.open(img_path) if os.path.exists(img_path) else None

        for i, meta in enumerate(self.col_meta):
            w = self.widgets[i]
            s_val, v_val = str(row[meta['src']]), str(row[meta['dest']])
            
            w['clean'].config(state=tk.NORMAL); w['clean'].delete("1.0", tk.END); w['clean'].insert("1.0", s_val); w['clean'].config(state=tk.DISABLED)
            w['entry'].delete("1.0", tk.END); w['entry'].insert("1.0", v_val if v_val.strip() else s_val)

            if base_img:
                x, y, width, height = self.CROP_CONFIG[i]
                cropped = base_img.crop((x, y, x + width, y + height))
                ratio = 260 / float(cropped.height)
                new_w = min(730, int(float(cropped.width) * ratio))
                cropped = cropped.resize((new_w, int(float(cropped.height) * (new_w/float(cropped.width)))), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(cropped)
                w['img'].config(image=tk_img); w['img'].image = tk_img
        
        self.flag_var.set(str(row.get("Flagged", "NO")) == "YES")
        self.widgets[0]['entry'].focus_set()

    def handle_tab(self, e): 
        self.hide_suggestions(); e.widget.tk_focusNext().focus_set(); return "break"
    def handle_shift_tab(self, e): 
        self.hide_suggestions(); e.widget.tk_focusPrev().focus_set(); return "break"
    
    def save_and_next_event(self, e): 
        if e.state & 0x0001: return "break"

        if self.suggestion_frame.winfo_viewable(): 
            self.select_suggestion()
            return "break"

        self.save_and_next()
        return "break"
    
    def go_back(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_row()
        else:
            messagebox.showinfo("Start", "You are at the first record.")
        return "break"

    def save_and_next(self):
        idx = self.current_index
        for i, meta in enumerate(self.col_meta):
            self.df.at[idx, meta['dest']] = self.widgets[i]['entry'].get("1.0", "end-1c").strip()
        self.df.at[idx, "Flagged"] = "YES" if self.flag_var.get() else "NO"
        self.df.to_csv(self.output_path, index=False)
        if self.current_index < len(self.df) - 1:
            self.current_index += 1; self.load_row()
        else: messagebox.showinfo("Done", "End of records.")

    def jump_to_row(self):
        try:
            val = int(self.row_entry.get())
            if 0 <= val < len(self.df): self.current_index = val; self.load_row()
        except: pass

if __name__ == "__main__":
    app = LocalDataReviewApp(tk.Tk(), "database_index.csv", "./images"); tk.mainloop()
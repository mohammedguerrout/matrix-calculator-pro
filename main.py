
# ----------------------------------------------------------
#  nom du programmer :  mohammed guerrout
# ----------------------------------------------------------

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import csv
import random
import time


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ACCENT_COLORS = {
    "🔵 Bleu": {"main": "#3A86FF", "hover": "#2563EB", "theme": "blue"},
    "🟢 Vert": {"main": "#22C55E", "hover": "#16A34A", "theme": "green"},
    "🟣 Sombre": {"main": "#8338EC", "hover": "#6B21A8", "theme": "dark-blue"},
}


class MatrixMath:
    """Toutes les opérations matricielles utilisées par l'application."""

    @staticmethod
    def get_minor(matrix, i, j):
        return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]

    @staticmethod
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for c in range(n):
            det += ((-1) ** c) * matrix[0][c] * MatrixMath.determinant(MatrixMath.get_minor(matrix, 0, c))
        return det

    @staticmethod
    def adjoint(matrix):
        n = len(matrix)
        if n == 1:
            return [[1]]
        adj = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                sign = (-1) ** (i + j)
                adj[j][i] = sign * MatrixMath.determinant(MatrixMath.get_minor(matrix, i, j))
        return adj

    @staticmethod
    def inverse(matrix):
        det = MatrixMath.determinant(matrix)
        if abs(det) < 1e-12:
            return None
        adj = MatrixMath.adjoint(matrix)
        n = len(matrix)
        return [[adj[i][j] / det for j in range(n)] for i in range(n)]

    @staticmethod
    def transpose(matrix):
        rows, cols = len(matrix), len(matrix[0])
        return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

    @staticmethod
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))

    @staticmethod
    def add(a, b):
        return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    @staticmethod
    def subtract(a, b):
        return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    @staticmethod
    def multiply(a, b):
        rows_a, cols_a = len(a), len(a[0])
        rows_b, cols_b = len(b), len(b[0])
        if cols_a != rows_b:
            return None
        result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
        for i in range(rows_a):
            for j in range(cols_b):
                result[i][j] = sum(a[i][k] * b[k][j] for k in range(cols_a))
        return result

    @staticmethod
    def scalar_multiply(matrix, scalar):
        return [[val * scalar for val in row] for row in matrix]

    @staticmethod
    def power(matrix, n):
        size = len(matrix)
        if n == 0:
            return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
        base = matrix
        if n < 0:
            base = MatrixMath.inverse(matrix)
            if base is None:
                return None
            n = -n
        result = [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
        for _ in range(n):
            result = MatrixMath.multiply(result, base)
        return result

    @staticmethod
    def rank(matrix):
        m = [row[:] for row in matrix]
        rows = len(m)
        cols = len(m[0]) if rows else 0
        r = 0
        for c in range(cols):
            pivot = None
            for i in range(r, rows):
                if abs(m[i][c]) > 1e-9:
                    pivot = i
                    break
            if pivot is None:
                continue
            m[r], m[pivot] = m[pivot], m[r]
            pivot_val = m[r][c]
            m[r] = [x / pivot_val for x in m[r]]
            for i in range(rows):
                if i != r and abs(m[i][c]) > 1e-9:
                    factor = m[i][c]
                    m[i] = [m[i][k] - factor * m[r][k] for k in range(cols)]
            r += 1
            if r == rows:
                break
        return r



class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip, text=self.text, justify="left", background="#1f1f1f",
                          foreground="white", relief="solid", borderwidth=1,
                          font=("Arial", 10), padx=6, pady=3)
        label.pack()

    def hide(self, _event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None



class LuxuryMatrixApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculatrice Matricielle Pro ✨")
        self.geometry("1150x950")
        self.minsize(950, 800)

        self.entries_a = []
        self.entries_b = []
        self.current_size = 3
        self.b_enabled = False
        self.decimals = 3
        self.history = []
        self.undo_stack = []
        self.accent = ACCENT_COLORS["🔵 Bleu"]

        self.vcmd = (self.register(self.validate_input), '%P')

        self.setup_menu()
        self.setup_ui()
        self.setup_shortcuts()
        self.generate_grid("3x3")

    
    def setup_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="💾 Sauvegarder la matrice A (Ctrl+S)", command=self.save_matrix)
        file_menu.add_command(label="📂 Charger une matrice (Ctrl+O)", command=self.load_matrix)
        file_menu.add_command(label="📤 Exporter le résultat en CSV", command=self.export_result_csv)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Quitter (Ctrl+Q)", command=self.quit)
        menubar.add_cascade(label="📁 Fichier", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="🗑️ Effacer tout (Ctrl+R)", command=self.clear_grid)
        edit_menu.add_command(label="🎲 Remplissage aléatoire (Ctrl+G)", command=self.fill_random)
        edit_menu.add_command(label="🔷 Matrice identité (Ctrl+I)", command=self.fill_identity)
        edit_menu.add_command(label="⬛ Matrice nulle", command=self.fill_zero)
        edit_menu.add_command(label="↩️ Annuler (Ctrl+Z)", command=self.undo)
        menubar.add_cascade(label="✏️ Édition", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="☀️ Mode Clair", command=lambda: self.set_theme_mode("Light"))
        view_menu.add_command(label="🌙 Mode Sombre", command=lambda: self.set_theme_mode("Dark"))
        view_menu.add_separator()
        for name in ACCENT_COLORS:
            view_menu.add_command(label=name, command=lambda n=name: self.set_accent(n))
        menubar.add_cascade(label="🎨 Affichage", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="⌨️ Raccourcis clavier", command=self.show_shortcuts)
        help_menu.add_command(label="ℹ️ À propos", command=self.show_about)
        menubar.add_cascade(label="❓ Aide", menu=help_menu)

        self.configure(menu=menubar)

    def setup_shortcuts(self):
        self.bind("<Control-d>", lambda e: self.show_determinant())
        self.bind("<Control-i>", lambda e: self.fill_identity())
        self.bind("<Control-t>", lambda e: self.show_transpose())
        self.bind("<Control-r>", lambda e: self.clear_grid())
        self.bind("<Control-g>", lambda e: self.fill_random())
        self.bind("<Control-s>", lambda e: self.save_matrix())
        self.bind("<Control-o>", lambda e: self.load_matrix())
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-q>", lambda e: self.quit())

    
    def validate_input(self, new_value):
        if new_value in ("", "-", ".", "-."):
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    
    def setup_ui(self):
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True)

        # --- Barre supérieure ---
        self.top_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.top_frame.pack(pady=20, padx=30, fill="x")

        self.theme_switch = ctk.CTkSwitch(self.top_frame, text="Mode Clair ☀️", font=("Arial", 14, "bold"),
                                           command=self.toggle_theme, onvalue="light", offvalue="dark")
        self.theme_switch.pack(side="left")

        self.title_label = ctk.CTkLabel(self.top_frame, text="🧮 Calculatrice Matricielle Pro",
                                         font=ctk.CTkFont(family="Arial", size=26, weight="bold"))
        self.title_label.pack(side="right")

        # --- Cadre des paramètres ---
        self.settings_frame = ctk.CTkFrame(self.main_scroll, corner_radius=15)
        self.settings_frame.pack(pady=10, padx=30, fill="x")

        self.size_var = ctk.StringVar(value="3x3")
        self.size_menu = ctk.CTkOptionMenu(self.settings_frame, values=["2x2", "3x3", "4x4", "5x5", "6x6", "7x7", "8x8"],
                                            variable=self.size_var, command=self.generate_grid,
                                            font=("Arial", 14, "bold"), width=100, dropdown_font=("Arial", 14))
        self.size_menu.pack(side="right", padx=10, pady=15)
        ctk.CTkLabel(self.settings_frame, text="📏 Taille :", font=("Arial", 15)).pack(side="right", padx=(20, 0), pady=15)

        self.b_switch = ctk.CTkSwitch(self.settings_frame, text="➕ Activer la matrice B", font=("Arial", 14, "bold"),
                                       command=self.toggle_matrix_b)
        self.b_switch.pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(self.settings_frame, text="🔢 Décimales :", font=("Arial", 14)).pack(side="left", padx=(20, 5))
        self.decimals_var = ctk.StringVar(value="3")
        self.decimals_menu = ctk.CTkOptionMenu(self.settings_frame, values=["0", "1", "2", "3", "4", "5", "6"],
                                                variable=self.decimals_var, width=60,
                                                command=lambda v: setattr(self, "decimals", int(v)))
        self.decimals_menu.pack(side="left", padx=5)

        # --- Cadres matrices A et B ---
        self.matrices_row = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.matrices_row.pack(pady=10, padx=30)

        self.matrix_card_a = ctk.CTkFrame(self.matrices_row, corner_radius=20, border_width=2, border_color="#3A86FF")
        self.matrix_card_a.pack(side="left", padx=15)
        ctk.CTkLabel(self.matrix_card_a, text="Matrice A", font=("Arial", 15, "bold")).pack(pady=(10, 0))
        self.matrix_inner_frame_a = ctk.CTkFrame(self.matrix_card_a, fg_color="transparent")
        self.matrix_inner_frame_a.pack(pady=20, padx=20)

        self.matrix_card_b = ctk.CTkFrame(self.matrices_row, corner_radius=20, border_width=2, border_color="#8338EC")
        ctk.CTkLabel(self.matrix_card_b, text="Matrice B", font=("Arial", 15, "bold")).pack(pady=(10, 0))
        self.matrix_inner_frame_b = ctk.CTkFrame(self.matrix_card_b, fg_color="transparent")
        self.matrix_inner_frame_b.pack(pady=20, padx=20)

        # --- Boutons rapides de remplissage ---
        self.quick_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.quick_frame.pack(pady=(5, 10))
        qbtn_font = ctk.CTkFont(family="Arial", size=13, weight="bold")
        quick_buttons = [
            ("🎲 Aléatoire", self.fill_random, "#F59E0B", "#B45309"),
            ("🔷 Identité", self.fill_identity, "#3A86FF", "#2563EB"),
            ("⬛ Nulle", self.fill_zero, "#64748B", "#475569"),
            ("↩️ Annuler", self.undo, "#94A3B8", "#64748B"),
        ]
        for i, (txt, cmd, col, hov) in enumerate(quick_buttons):
            b = ctk.CTkButton(self.quick_frame, text=txt, font=qbtn_font, command=cmd,
                               fg_color=col, hover_color=hov, width=120)
            b.grid(row=0, column=i, padx=6)

       
        self.buttons_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.buttons_frame.pack(pady=10, padx=30)

        btn_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        single_ops = [
            ("📉 Déterminant", self.show_determinant, "#3A86FF", "#2563EB", "Calcule le déterminant de A (Ctrl+D)"),
            ("🔄 Adjointe", self.show_adjoint, "#8338EC", "#6B21A8", "Calcule la matrice adjointe de A"),
            ("✨ Inverse", self.show_inverse, "#FF006E", "#BE123C", "Calcule l'inverse de A"),
            ("🔁 Transposée", self.show_transpose, "#06B6D4", "#0E7490", "Transpose la matrice A (Ctrl+T)"),
            ("Σ Trace", self.show_trace, "#10B981", "#047857", "Somme de la diagonale de A"),
            ("🏗️ Rang", self.show_rank, "#F59E0B", "#B45309", "Calcule le rang de A"),
        ]
        for i, (txt, cmd, col, hov, tip) in enumerate(single_ops):
            b = ctk.CTkButton(self.buttons_frame, text=txt, font=btn_font, command=cmd,
                               fg_color=col, hover_color=hov, width=150)
            b.grid(row=0, column=i, padx=8, pady=6)
            ToolTip(b, tip)

        
        self.power_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.power_frame.pack(pady=(0, 10))
        ctk.CTkLabel(self.power_frame, text="🔺 Puissance n :", font=("Arial", 14)).grid(row=0, column=0, padx=6)
        self.power_entry = ctk.CTkEntry(self.power_frame, width=60, justify="center")
        self.power_entry.insert(0, "2")
        self.power_entry.grid(row=0, column=1, padx=6)
        ctk.CTkButton(self.power_frame, text="🔺 Calculer A^n", font=btn_font, command=self.show_power,
                      fg_color="#EF4444", hover_color="#B91C1C", width=150).grid(row=0, column=2, padx=10)

        ctk.CTkLabel(self.power_frame, text="✖️ Scalaire :", font=("Arial", 14)).grid(row=0, column=3, padx=(20, 6))
        self.scalar_entry = ctk.CTkEntry(self.power_frame, width=60, justify="center")
        self.scalar_entry.insert(0, "2")
        self.scalar_entry.grid(row=0, column=4, padx=6)
        ctk.CTkButton(self.power_frame, text="✖️ k · A", font=btn_font, command=self.show_scalar_multiply,
                      fg_color="#EAB308", hover_color="#A16207", width=120).grid(row=0, column=5, padx=10)

        
        self.dual_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.dual_frame.pack(pady=(0, 15))
        dual_ops = [
            ("➕ A + B", self.show_add, "#22C55E", "#16A34A"),
            ("➖ A − B", self.show_subtract, "#F97316", "#C2410C"),
            ("✖️ A × B", self.show_multiply, "#8B5CF6", "#6D28D9"),
        ]
        self.dual_buttons = []
        for i, (txt, cmd, col, hov) in enumerate(dual_ops):
            b = ctk.CTkButton(self.dual_frame, text=txt, font=btn_font, command=cmd,
                               fg_color=col, hover_color=hov, width=150, state="disabled")
            b.grid(row=0, column=i, padx=8, pady=6)
            self.dual_buttons.append(b)

   
        self.result_card = ctk.CTkFrame(self.main_scroll, corner_radius=15)
        self.result_card.pack(pady=10, padx=30, fill="both")

        result_header = ctk.CTkFrame(self.result_card, fg_color="transparent")
        result_header.pack(fill="x", padx=20, pady=(10, 0))
        self.result_title = ctk.CTkLabel(result_header, text="📊 Écran des Résultats", font=("Arial", 16, "bold"), text_color="#3A86FF")
        self.result_title.pack(side="left")
        ctk.CTkButton(result_header, text="📋 Copier", font=("Arial", 12, "bold"), width=90,
                      command=self.copy_result, fg_color="#475569", hover_color="#334155").pack(side="right")

        self.output_textbox = ctk.CTkTextbox(self.result_card, height=180, font=ctk.CTkFont(family="Consolas", size=16),
                                              state="disabled", fg_color="transparent", text_color=("#111", "#FFF"))
        self.output_textbox.pack(pady=10, padx=20, fill="both")

        
        self.history_card = ctk.CTkFrame(self.main_scroll, corner_radius=15)
        self.history_card.pack(pady=(0, 20), padx=30, fill="both")
        ctk.CTkLabel(self.history_card, text="🕘 Historique des opérations", font=("Arial", 16, "bold"), text_color="#8338EC").pack(anchor="w", padx=20, pady=(10, 0))
        self.history_frame = ctk.CTkScrollableFrame(self.history_card, height=140, fg_color="transparent")
        self.history_frame.pack(pady=10, padx=20, fill="both")

       
        self.status_bar = ctk.CTkLabel(self, text="✅ Prêt", font=("Arial", 12), anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=4)

    
    def toggle_theme(self):
        if self.theme_switch.get() == "light":
            self.set_theme_mode("Light")
        else:
            self.set_theme_mode("Dark")

    def set_theme_mode(self, mode):
        ctk.set_appearance_mode(mode)
        if mode == "Light":
            self.theme_switch.select()
            self.theme_switch.configure(text="Mode Sombre 🌙")
        else:
            self.theme_switch.deselect()
            self.theme_switch.configure(text="Mode Clair ☀️")
        self.set_status(f"🎨 Thème changé vers le mode {'Clair' if mode == 'Light' else 'Sombre'}")

    def set_accent(self, name):
        self.accent = ACCENT_COLORS[name]
        messagebox.showinfo("🎨 Couleur", f"Redémarrez l'application pour appliquer complètement le thème {name}.")
        self.set_status(f"🎨 Couleur d'accentuation choisie : {name}")

  
    def move_focus(self, entries, r, c):
        size = len(entries)
        if 0 <= r < size and 0 <= c < size:
            entries[r][c].focus_set()
            entries[r][c].select_range(0, 'end')

   
    def generate_grid(self, choice):
        self.current_size = int(choice.split('x')[0])
        self.entries_a = self._build_grid(self.matrix_inner_frame_a, self.current_size)
        if self.b_enabled:
            self.entries_b = self._build_grid(self.matrix_inner_frame_b, self.current_size)
        self.set_status(f"✨ Espace de travail créé pour une matrice {self.current_size}x{self.current_size}")
        self.entries_a[0][0].focus_set()

    def _build_grid(self, frame, size):
        for widget in frame.winfo_children():
            widget.destroy()
        entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                ent = ctk.CTkEntry(frame, width=65, height=48,
                                    font=ctk.CTkFont(size=17, weight="bold"), justify="center", corner_radius=10,
                                    validate="key", validatecommand=self.vcmd)
                ent.grid(row=i, column=j, padx=6, pady=6)
                ent.insert(0, "0")
                ent.bind("<Up>", lambda e, r=i, c=j, en=None: self.move_focus(entries, r - 1, c))
                ent.bind("<Down>", lambda e, r=i, c=j: self.move_focus(entries, r + 1, c))
                ent.bind("<Left>", lambda e, r=i, c=j: self.move_focus(entries, r, c - 1))
                ent.bind("<Right>", lambda e, r=i, c=j: self.move_focus(entries, r, c + 1))
                ent.bind("<FocusIn>", lambda e, widget=ent: widget.select_range(0, 'end'))
                row_entries.append(ent)
            entries.append(row_entries)
        return entries

    def toggle_matrix_b(self):
        self.b_enabled = self.b_switch.get()
        if self.b_enabled:
            self.matrix_card_b.pack(side="left", padx=15)
            self.entries_b = self._build_grid(self.matrix_inner_frame_b, self.current_size)
            for b in self.dual_buttons:
                b.configure(state="normal")
            self.set_status("➕ Matrice B activée")
        else:
            self.matrix_card_b.pack_forget()
            for b in self.dual_buttons:
                b.configure(state="disabled")
            self.set_status("Matrice B désactivée")

  
    def _push_undo(self):
        self.undo_stack.append(self.get_matrix_safe(self.entries_a))
        if len(self.undo_stack) > 15:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            self.set_status("⚠️ Rien à annuler")
            return
        previous = self.undo_stack.pop()
        if previous is None:
            return
        for i in range(self.current_size):
            for j in range(self.current_size):
                self.entries_a[i][j].delete(0, 'end')
                val = previous[i][j]
                self.entries_a[i][j].insert(0, self._fmt_num(val))
        self.set_status("↩️ Dernière opération annulée")

    def clear_grid(self):
        self._push_undo()
        for i in range(self.current_size):
            for j in range(self.current_size):
                self.entries_a[i][j].delete(0, 'end')
                self.entries_a[i][j].insert(0, "0")
        self.print_to_output("🗑️ Effacement", "Toutes les valeurs de la matrice A ont été réinitialisées à 0.")
        self.entries_a[0][0].focus_set()

    def fill_zero(self):
        self._push_undo()
        for i in range(self.current_size):
            for j in range(self.current_size):
                self.entries_a[i][j].delete(0, 'end')
                self.entries_a[i][j].insert(0, "0")
        self.set_status("⬛ Matrice A remplie de zéros")

    def fill_identity(self):
        self._push_undo()
        for i in range(self.current_size):
            for j in range(self.current_size):
                self.entries_a[i][j].delete(0, 'end')
                self.entries_a[i][j].insert(0, "1" if i == j else "0")
        self.set_status("🔷 Matrice identité générée")

    def fill_random(self):
        self._push_undo()
        for i in range(self.current_size):
            for j in range(self.current_size):
                self.entries_a[i][j].delete(0, 'end')
                self.entries_a[i][j].insert(0, str(random.randint(-9, 9)))
        self.set_status("🎲 Matrice A remplie aléatoirement")

  
    def get_matrix(self, entries=None):
        entries = entries or self.entries_a
        matrix = []
        for i in range(self.current_size):
            row = []
            for j in range(self.current_size):
                val = entries[i][j].get()
                if val in ("", "-", ".", "-."):
                    val = "0"
                row.append(float(val))
            matrix.append(row)
        return matrix

    def get_matrix_safe(self, entries):
        try:
            return self.get_matrix(entries)
        except Exception:
            return None

    def _fmt_num(self, val):
        if float(val).is_integer():
            return str(int(val))
        return f"{val:.{self.decimals}f}".rstrip('0').rstrip('.')


    def print_to_output(self, title, content, add_history=True):
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("0.0", "end")

        self.result_title.configure(text=f"📊 {title}")
        self.output_textbox.insert("end", "\n")

        text_lines = []
        if isinstance(content, list):
            for row in content:
                formatted_row = "    ".join(
                    [f"{val:8.{self.decimals}f}".rstrip('0').rstrip('.') if isinstance(val, float) else f"{val:8}"
                     for val in row]
                )
                line = f"   │  {formatted_row}  │"
                self.output_textbox.insert("end", line + "\n\n")
                text_lines.append(line)
        else:
            self.output_textbox.insert("end", f"   {content}\n")
            text_lines.append(str(content))

        self.output_textbox.configure(state="disabled")
        self.set_status(f"✅ {title} calculé(e) avec succès")

        if add_history:
            self._add_history(title, "\n".join(text_lines))

    def _add_history(self, title, text):
        stamp = time.strftime("%H:%M:%S")
        entry_text = f"{stamp} — {title}"
        row = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=f"🕘 {entry_text}", font=("Arial", 12), anchor="w").pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(row, text="🔁 Revoir", width=80, font=("Arial", 11, "bold"),
                      command=lambda t=title, c=text: self._restore_history(t, c)).pack(side="right", padx=5)
        self.history.append((title, text))
        if len(self.history_frame.winfo_children()) > 20:
            self.history_frame.winfo_children()[0].destroy()

    def _restore_history(self, title, text):
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("0.0", "end")
        self.result_title.configure(text=f"📊 {title} (Historique)")
        self.output_textbox.insert("end", "\n" + text + "\n")
        self.output_textbox.configure(state="disabled")
        self.set_status(f"🔁 Résultat restauré depuis l'historique : {title}")

    def copy_result(self):
        content = self.output_textbox.get("0.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.set_status("📋 Résultat copié dans le presse-papiers")
        else:
            self.set_status("⚠️ Aucun résultat à copier")

    def set_status(self, text):
        self.status_bar.configure(text=text)

  
    def show_determinant(self):
        try:
            mat = self.get_matrix(self.entries_a)
            res = MatrixMath.determinant(mat)
            self.print_to_output("Déterminant (Det A)", f"Résultat = {round(res, 6)}")
        except Exception as e:
            self._error(e)

    def show_adjoint(self):
        try:
            mat = self.get_matrix(self.entries_a)
            self.print_to_output("Matrice Adjointe de A", MatrixMath.adjoint(mat))
        except Exception as e:
            self._error(e)

    def show_inverse(self):
        try:
            mat = self.get_matrix(self.entries_a)
            res = MatrixMath.inverse(mat)
            if res is None:
                self.print_to_output("⚠️ Alerte Mathématique", "La matrice A n'a pas d'inverse (déterminant nul).")
            else:
                self.print_to_output("Matrice Inverse de A", res)
        except Exception as e:
            self._error(e)

    def show_transpose(self):
        try:
            mat = self.get_matrix(self.entries_a)
            self.print_to_output("Transposée de A", MatrixMath.transpose(mat))
        except Exception as e:
            self._error(e)

    def show_trace(self):
        try:
            mat = self.get_matrix(self.entries_a)
            self.print_to_output("Trace de A", f"Résultat = {round(MatrixMath.trace(mat), 6)}")
        except Exception as e:
            self._error(e)

    def show_rank(self):
        try:
            mat = self.get_matrix(self.entries_a)
            self.print_to_output("Rang de A", f"Résultat = {MatrixMath.rank(mat)}")
        except Exception as e:
            self._error(e)

    def show_power(self):
        try:
            n = int(self.power_entry.get())
            mat = self.get_matrix(self.entries_a)
            res = MatrixMath.power(mat, n)
            if res is None:
                self.print_to_output("⚠️ Alerte Mathématique", "Impossible : matrice non inversible pour une puissance négative.")
            else:
                self.print_to_output(f"A puissance {n}", res)
        except ValueError:
            messagebox.showerror("Erreur ❌", "Veuillez entrer un entier valide pour la puissance n.")
        except Exception as e:
            self._error(e)

    def show_scalar_multiply(self):
        try:
            k = float(self.scalar_entry.get())
            mat = self.get_matrix(self.entries_a)
            self.print_to_output(f"{k} · A", MatrixMath.scalar_multiply(mat, k))
        except ValueError:
            messagebox.showerror("Erreur ❌", "Veuillez entrer un scalaire numérique valide.")
        except Exception as e:
            self._error(e)

   
    def show_add(self):
        try:
            a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
            self.print_to_output("A + B", MatrixMath.add(a, b))
        except Exception as e:
            self._error(e)

    def show_subtract(self):
        try:
            a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
            self.print_to_output("A − B", MatrixMath.subtract(a, b))
        except Exception as e:
            self._error(e)

    def show_multiply(self):
        try:
            a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
            res = MatrixMath.multiply(a, b)
            if res is None:
                self.print_to_output("⚠️ Alerte Mathématique", "Dimensions incompatibles pour la multiplication A × B.")
            else:
                self.print_to_output("A × B", res)
        except Exception as e:
            self._error(e)

    def _error(self, e):
        messagebox.showerror("Erreur ❌", f"Une erreur est survenue :\n{e}")
        self.set_status("❌ Erreur lors du calcul")

    def save_matrix(self):
        try:
            mat = self.get_matrix(self.entries_a)
        except Exception as e:
            return self._error(e)
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("Fichier JSON", "*.json")],
                                             title="💾 Sauvegarder la matrice A")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"size": self.current_size, "matrix": mat}, f, ensure_ascii=False, indent=2)
        self.set_status(f"💾 Matrice A sauvegardée dans {path}")

    def load_matrix(self):
        path = filedialog.askopenfilename(filetypes=[("Fichier JSON", "*.json")],
                                           title="📂 Charger une matrice")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            size = data["size"]
            mat = data["matrix"]
            self.size_var.set(f"{size}x{size}")
            self.generate_grid(f"{size}x{size}")
            for i in range(size):
                for j in range(size):
                    self.entries_a[i][j].delete(0, 'end')
                    self.entries_a[i][j].insert(0, self._fmt_num(mat[i][j]))
            self.set_status(f"📂 Matrice chargée depuis {path}")
        except Exception as e:
            self._error(e)

    def export_result_csv(self):
        if not self.history:
            return messagebox.showwarning("⚠️ Attention", "Aucun résultat à exporter pour le moment.")
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("Fichier CSV", "*.csv")],
                                             title="📤 Exporter le résultat")
        if not path:
            return
        last_title, last_text = self.history[-1]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([last_title])
            for line in last_text.split("\n"):
                writer.writerow([line])
        self.set_status(f"📤 Résultat exporté vers {path}")

 
    def show_shortcuts(self):
        text = (
            "⌨️ Ctrl+D : Déterminant\n"
            "⌨️ Ctrl+I : Matrice identité\n"
            "⌨️ Ctrl+T : Transposée\n"
            "⌨️ Ctrl+R : Effacer\n"
            "⌨️ Ctrl+G : Remplissage aléatoire\n"
            "⌨️ Ctrl+Z : Annuler\n"
            "⌨️ Ctrl+S : Sauvegarder\n"
            "⌨️ Ctrl+O : Charger\n"
            "⌨️ Ctrl+Q : Quitter\n"
            "⬆️⬇️⬅️➡️ : Navigation entre les cases"
        )
        messagebox.showinfo("⌨️ Raccourcis clavier", text)

    def show_about(self):
        messagebox.showinfo(
            "ℹ️ À propos",
            "🧮 Calculatrice Matricielle Pro ✨\n\n"
            "Une application complète pour :\n"
            "• Déterminant, Adjointe, Inverse, Transposée\n"
            "• Trace, Rang, Puissance, Multiplication scalaire\n"
            "• Addition, Soustraction, Multiplication de 2 matrices\n"
            "• Sauvegarde / Chargement / Export CSV\n"
            "• Historique complet des opérations\n\n"
            "Développée avec ❤️ en Python + CustomTkinter."
        )


if __name__ == "__main__":
    app = LuxuryMatrixApp()
    app.mainloop()
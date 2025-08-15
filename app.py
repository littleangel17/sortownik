# -*- coding: utf-8 -*- 

"""
Aplikacja Desktopowa do Zarządzania Danymi Pomiarowymi
Wersja: 2.0
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class DataManagerApp:
    """
    Główna klasa aplikacji 2-w-1: Sortownik Plików i Analizator Danych .sit.
    Zarządza interfejsem graficznym, logiką biznesową i interakcją z użytkownikiem.
    """

    def __init__(self, master):
        """
        Inicjalizuje główne okno aplikacji i wszystkie jego komponenty.
        """
        self.master = master
        self.master.title("Menedżer Danych Pomiarowych v2.0")
        self.master.geometry("700x500")
        self.master.minsize(600, 400)

        self.target_folder = tk.StringVar()

        style = ttk.Style(self.master)
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        """
        Tworzy i rozmieszcza wszystkie widżety w oknie aplikacji.
        """
        # --- Ramka górna: Wybór folderu ---
        folder_frame = ttk.Frame(self.master, padding="10")
        folder_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(folder_frame, text="Folder roboczy:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))

        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.target_folder, state='readonly', font=('Helvetica', 10))
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.select_button = ttk.Button(folder_frame, text="Wybierz Folder", command=self.select_folder)
        self.select_button.pack(side=tk.LEFT, padx=(10, 0))

        # --- Ramka środkowa: Panel Kontrolny ---
        control_frame = ttk.Frame(self.master, padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.sort_button = ttk.Button(control_frame, text="1. Uporządkuj Pliki w Folderze", command=self.sort_files, state='disabled')
        self.sort_button.pack(pady=5, fill=tk.X)

        self.analyze_button = ttk.Button(control_frame, text="2. Przetwórz .sit i Generuj Excel", command=self.prepare_and_analyze_sit_files, state='disabled')
        self.analyze_button.pack(pady=5, fill=tk.X)

        # --- Ramka dolna: Dziennik Operacji ---
        log_frame = ttk.Frame(self.master, padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        log_label = ttk.Label(log_frame, text="Dziennik operacji:", font=('Helvetica', 10, 'bold'))
        log_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        self.log_text = tk.Text(log_frame, height=15, state='disabled', wrap=tk.WORD, font=('Courier New', 9), bg="#f0f0f0")
        self.log_text.grid(row=1, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        """Dodaje wpis do pola logów aplikacji."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.master.update_idletasks()

    def set_buttons_state(self, state):
        """Włącza lub wyłącza przyciski operacji."""
        new_state = 'disabled' if state == 'disabled' else 'normal'
        self.sort_button.config(state=new_state)
        self.analyze_button.config(state=new_state)
        self.select_button.config(state=new_state)

    def select_folder(self):
        """Otwiera okno dialogowe do wyboru folderu."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_folder.set(folder_selected)
            self.set_buttons_state('normal')
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            self.log(f"Wybrano folder: {folder_selected}")
            self.log("Wybierz operację do wykonania.")
        else:
            self.log("Anulowano wybór folderu.")

    def sort_files(self):
        """MODUŁ 1: Sortuje pliki w wybranym folderze na podstawie ich rozszerzeń."""
        target_dir = self.target_folder.get()
        if not os.path.isdir(target_dir):
            messagebox.showerror("Błąd", "Wybrana ścieżka nie jest prawidłowym folderem.")
            return

        self.log("\n>>> Rozpoczynanie operacji porządkowania (Moduł 1)...")
        self.set_buttons_state('disabled')

        try:
            files_moved = 0
            all_items = os.listdir(target_dir)

            for item_name in all_items:
                item_path = os.path.join(target_dir, item_name)

                if os.path.isfile(item_path):
                    _, extension = os.path.splitext(item_name)
                    subdir_name = "Pliki_Bez_Rozszerzenia" if not extension else extension[1:].lower()
                    
                    if subdir_name in ['py', 'exe', 'md', 'gitignore']:
                        continue

                    dest_dir = os.path.join(target_dir, subdir_name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                        self.log(f"Utworzono folder: {subdir_name}")

                    shutil.move(item_path, os.path.join(dest_dir, item_name))
                    self.log(f"Przeniesiono: '{item_name}' -> do folderu '{subdir_name}'")
                    files_moved += 1
            
            if files_moved > 0:
                self.log(f"\n>>> Zakończono! Przeniesiono łącznie {files_moved} plików.")
                messagebox.showinfo("Sukces", f"Operacja zakończona pomyślnie.\nUporządkowano {files_moved} plików.")
            else:
                self.log("\n>>> Zakończono! Nie znaleziono plików do przeniesienia.")
                messagebox.showinfo("Informacja", "W wybranym folderze nie znaleziono plików do uporządkowania.")

        except Exception as e:
            self.log(f"!!! Wystąpił krytyczny błąd: {e}")
            messagebox.showerror("Błąd Krytyczny", f"Wystąpił nieoczekiwany błąd:\n{e}")
        finally:
            self.set_buttons_state('normal')

    def prepare_and_analyze_sit_files(self):
        """MODUŁ 2: Przetwarza pliki .sit i generuje plik Excel."""
        target_dir = self.target_folder.get()
        if not os.path.isdir(target_dir):
            messagebox.showerror("Błąd", "Wybrana ścieżka nie jest prawidłowym folderem.")
            return

        self.log("\n>>> Rozpoczynanie przetwarzania plików .sit (Moduł 2)...")
        self.set_buttons_state('disabled')
        
        converted_dir_name = "txt_z_sit"
        converted_dir_path = os.path.join(target_dir, converted_dir_name)

        try:
            # --- Etap 1: Konwersja .sit do .txt ---
            self.log("Etap 1: Konwersja plików .sit na .txt")
            if not os.path.exists(converted_dir_path):
                os.makedirs(converted_dir_path)
                self.log(f"Utworzono folder docelowy: {converted_dir_name}")

            sit_files_found = []
            for dirpath, _, filenames in os.walk(target_dir):
                # Ignoruj folder docelowy, aby uniknąć pętli
                if os.path.commonpath([dirpath, converted_dir_path]) == converted_dir_path:
                    continue
                for filename in filenames:
                    if filename.lower().endswith(".sit"):
                        sit_files_found.append(os.path.join(dirpath, filename))

            if not sit_files_found:
                self.log("Nie znaleziono żadnych plików .sit do przetworzenia.")
                messagebox.showinfo("Informacja", "Nie znaleziono plików .sit w wybranym folderze i jego podfolderach.")
                self.set_buttons_state('normal')
                return

            self.log(f"Znaleziono {len(sit_files_found)} plików .sit. Rozpoczynam kopiowanie i zmianę rozszerzenia...")
            for src_path in sit_files_found:
                base_filename = os.path.basename(src_path)
                new_filename = os.path.splitext(base_filename)[0] + ".txt"
                dest_path = os.path.join(converted_dir_path, new_filename)
                shutil.copy2(src_path, dest_path)
                self.log(f"Skopiowano: '{base_filename}' -> '{os.path.join(converted_dir_name, new_filename)}'")

            # --- Etap 2: Analiza i Agregacja ---
            self.log("\nEtap 2: Analiza plików .txt i generowanie pliku Excel...")
            output_excel_file = os.path.join(target_dir, "wyniki.xlsx")
            
            self.parse_and_save_to_excel(converted_dir_path, output_excel_file)

        except Exception as e:
            self.log(f"!!! Wystąpił krytyczny błąd: {e}")
            messagebox.showerror("Błąd Krytyczny", f"Wystąpił nieoczekiwany błąd:\n{e}")
        finally:
            self.set_buttons_state('normal')

    def parse_and_save_to_excel(self, source_directory, output_excel_file):
        """Parsuje pliki .txt ze wskazanego folderu i zapisuje dane do pliku Excel."""
        all_data = {}
        
        txt_files = [f for f in os.listdir(source_directory) if f.endswith(".txt")]

        if not txt_files:
            self.log("Ostrzeżenie: W folderze 'txt_z_sit' nie ma plików .txt do analizy.")
            messagebox.showwarning("Brak Danych", "Nie znaleziono plików .txt do przetworzenia w folderze 'txt_z_sit'.")
            return

        self.log(f"Znaleziono {len(txt_files)} plików .txt do analizy.")

        for filename in txt_files:
            file_path = os.path.join(source_directory, filename)
            sheet_name = os.path.splitext(filename)[0]
            # Ograniczenie długości nazwy arkusza do 31 znaków (limit Excela)
            sheet_name = sheet_name[:31]

            try:
                data = pd.read_csv(file_path, sep='\s+', header=None, skiprows=1)
                if data.shape[1] >= 3:
                    data = data.iloc[:, :3]
                    data.columns = ['Time (ps)', 'Rad THz', 'Rad Time']
                    all_data[sheet_name] = data
                else:
                    self.log(f"Ostrzeżenie: Plik '{filename}' ma nieprawidłowy format (mniej niż 3 kolumny) i został pominięty.")
            except Exception as e:
                self.log(f"Błąd podczas przetwarzania pliku '{filename}': {e}")

        if not all_data:
            self.log("Nie udało się przetworzyć żadnych plików. Sprawdź format plików .txt.")
            messagebox.showerror("Błąd Analizy", "Nie udało się przetworzyć żadnych plików. Sprawdź logi, aby uzyskać więcej informacji.")
            return

        sorted_sheet_names = sorted(all_data.keys())
        with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
            for sheet_name in sorted_sheet_names:
                all_data[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

        self.log(f"\n>>> Zakończono! Pomyślnie zapisano dane do pliku '{os.path.basename(output_excel_file)}'")
        self.log(f"Liczba przetworzonych plików i utworzonych arkuszy: {len(sorted_sheet_names)}")
        messagebox.showinfo("Sukces", f"Pomyślnie utworzono plik '{os.path.basename(output_excel_file)}' z {len(sorted_sheet_names)} arkuszami.")


def main():
    """Główny punkt wejścia do aplikacji."""
    try:
        import openpyxl
    except ImportError:
        messagebox.showerror(
            "Brak zależności",
            "Biblioteka 'openpyxl' nie jest zainstalowana. Proszę ją zainstalować komendą:\n\npip install openpyxl"
        )
        return
        
    root = tk.Tk()
    app = DataManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
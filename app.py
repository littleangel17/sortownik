# -*- coding: utf-8 -*-

"""
Aplikacja Desktopowa do Porządkowania Danych Pomiarowych
"""

import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Import biblioteki Pandas zgodnie z wymaganiami projektu.
# Na tym etapie nie jest ona używana do sortowania plików,
# ale jest gotowa do przyszłej implementacji funkcji analizy danych.
import pandas as pd


class FileSorterApp:
    """
    Główna klasa aplikacji do sortowania plików w wybranym folderze.
    Zarządza interfejsem graficznym, logiką biznesową i interakcją z użytkownikiem.
    """

    def __init__(self, master):
        """
        Inicjalizuje główne okno aplikacji i wszystkie jego komponenty.
        """
        self.master = master
        self.master.title("Aplikacja do Porządkowania Danych v1.1")
        self.master.geometry("700x500")
        self.master.minsize(600, 400)

        # Zmienna przechowująca ścieżkę do wybranego folderu
        self.target_folder = tk.StringVar()

        # Ustawienie stylu dla widżetów
        style = ttk.Style(self.master)
        style.theme_use('clam')

        # Główne ramki interfejsu
        self.create_widgets()

    def create_widgets(self):
        """
        Tworzy i rozmieszcza wszystkie widżety w oknie aplikacji.
        """
        # --- Ramka górna: Wybór folderu ---
        folder_frame = ttk.Frame(self.master, padding="10")
        folder_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(folder_frame, text="Folder do uporządkowania:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))

        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.target_folder, state='readonly', font=('Helvetica', 10))
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.select_button = ttk.Button(folder_frame, text="Wybierz folder", command=self.select_folder)
        self.select_button.pack(side=tk.LEFT, padx=(10, 0))

        # --- Ramka środkowa: Panel Kontrolny ---
        control_frame = ttk.Frame(self.master, padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.sort_button = ttk.Button(control_frame, text="Uporządkuj Pliki", command=self.sort_files, state='disabled')
        self.sort_button.pack(pady=5, fill=tk.X)

        # --- Ramka dolna: Logi / Konsola (POPRAWIONA SEKCJA) ---
        log_frame = ttk.Frame(self.master, padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Konfiguracja siatki (grid) wewnątrz ramki 'log_frame'
        # Kolumna 0 (z polem tekstowym) będzie się rozszerzać
        log_frame.grid_columnconfigure(0, weight=1)
        # Wiersz 1 (z polem tekstowym i paskiem przewijania) będzie się rozszerzać
        log_frame.grid_rowconfigure(1, weight=1)

        # Etykieta umieszczona za pomocą grid
        log_label = ttk.Label(log_frame, text="Dziennik operacji:", font=('Helvetica', 10, 'bold'))
        log_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        # Pole tekstowe umieszczone za pomocą grid
        self.log_text = tk.Text(log_frame, height=15, state='disabled', wrap=tk.WORD, font=('Courier New', 9), bg="#f0f0f0")
        self.log_text.grid(row=1, column=0, sticky="nsew")
        
        # Pasek przewijania umieszczony za pomocą grid
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        """
        Dodaje wpis do pola logów aplikacji.
        """
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.master.update_idletasks() # Odświeża interfejs

    def select_folder(self):
        """
        Otwiera okno dialogowe do wyboru folderu i aktualizuje interfejs.
        """
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_folder.set(folder_selected)
            self.sort_button.config(state='normal')
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            self.log(f"Wybrano folder: {folder_selected}")
            self.log("Naciśnij 'Uporządkuj Pliki', aby rozpocząć sortowanie.")
        else:
            self.log("Anulowano wybór folderu.")

    def sort_files(self):
        """
        Główna funkcja wywołująca logikę sortowania plików.
        """
        target_dir = self.target_folder.get()
        if not os.path.isdir(target_dir):
            messagebox.showerror("Błąd", "Wybrana ścieżka nie jest prawidłowym folderem.")
            return

        self.log("\n>>> Rozpoczynanie operacji porządkowania...")
        self.sort_button.config(state='disabled')
        self.select_button.config(state='disabled')

        try:
            files_moved = 0
            # Pobranie listy wszystkich elementów w folderze
            all_items = os.listdir(target_dir)

            for item_name in all_items:
                item_path = os.path.join(target_dir, item_name)

                # Przetwarzaj tylko pliki, ignoruj istniejące foldery
                if os.path.isfile(item_path):
                    # Podział na nazwę i rozszerzenie
                    filename, extension = os.path.splitext(item_name)

                    if not extension:
                        # Obsługa plików bez rozszerzenia ("plik")
                        subdir_name = "Pliki_Bez_Rozszerzenia"
                    else:
                        # Normalizacja nazwy folderu: usuwamy kropkę i zmieniamy na małe litery
                        subdir_name = extension[1:].lower()

                    # Utworzenie ścieżki do folderu docelowego
                    dest_dir = os.path.join(target_dir, subdir_name)

                    # Utworzenie folderu docelowego, jeśli nie istnieje
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                        self.log(f"Utworzono folder: {subdir_name}")

                    # Przeniesienie pliku
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
            # Ponowne włączenie przycisków po zakończeniu operacji
            self.sort_button.config(state='normal')
            self.select_button.config(state='normal')


def main():
    """
    Główny punkt wejścia do aplikacji.
    """
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

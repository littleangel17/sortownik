# Koncepcja Rozwoju Aplikacji - Wersja 2.0

## 1. Wprowadzenie: Zintegrowane Narzędzie Danych

Projekt ewoluuje w zintegrowane narzędzie 2-w-1, łączące ogólną organizację plików z dedykowanym procesem przetwarzania i analizy danych. Aplikacja połączy logikę z `app.py` (sortowanie) i `parse.py` (analiza), dodając nowy, kluczowy krok przygotowania danych.

## 2. Główne Moduły Funkcjonalne

Aplikacja będzie posiadać dwa odrębne, ale komplementarne moduły dostępne z jednego interfejsu.

### Moduł 1: Sortownik Plików

*   **Cel:** Szybkie porządkowanie dowolnego folderu.
*   **Logika:** Działa identycznie jak w pierwotnej wersji `app.py`. Użytkownik wybiera folder, a aplikacja automatycznie sortuje wszystkie znajdujące się w nim pliki do podfolderów nazwanych według ich rozszerzeń (`.pdf` -> `/pdf/`, `.jpg` -> `/jpg/` itd.).

### Moduł 2: Analizator Plików `.sit`

*   **Cel:** Przetworzenie surowych danych z plików `.sit` i zagregowanie ich w jednym pliku Excel.
*   **Logika:** Ten moduł będzie działał w dwóch automatycznych etapach:
    1.  **Etap Konwersji (`.sit` -> `.txt`):**
        *   Aplikacja rekursywnie przeszukuje wybrany folder w poszukiwaniu wszystkich plików z rozszerzeniem `.sit`.
        *   Wewnątrz folderu głównego tworzony jest nowy podfolder o nazwie `txt_z_sit`.
        *   Każdy znaleziony plik `.sit` jest **kopiowany** do folderu `txt_z_sit`.
        *   Podczas kopiowania, rozszerzenie pliku jest **zmieniane z `.sit` na `.txt`**. (np. `pomiar1.sit` staje się `pomiar1.txt` wewnątrz `txt_z_sit`).
    2.  **Etap Analizy i Agregacji (`.txt` -> `.xlsx`):**
        *   Po zakończeniu konwersji, aplikacja automatycznie uruchamia logikę z `parse.py`.
        *   **Źródłem danych dla parsera jest wyłącznie folder `txt_z_sit`** stworzony w poprzednim etapie.
        *   Parser przetwarza wszystkie pliki `.txt` z tego folderu, tworząc z każdego osobny arkusz w pliku Excel.
        *   Wynikowy plik o nazwie `wyniki.xlsx` jest zapisywany w głównym, wybranym przez użytkownika folderze.

## 3. Interfejs Użytkownika i Przepływ Pracy

1.  Użytkownik uruchamia aplikację i widzi jedno okno.
2.  Klika **"Wybierz Folder"**, aby wskazać katalog do pracy.
3.  Po wybraniu folderu, aktywują się dwa przyciski:
    *   **"1. Uporządkuj Pliki"** (uruchamia Moduł 1)
    *   **"2. Przetwórz .sit i Generuj Excel"** (uruchamia Moduł 2 z jego dwoma etapami)
4.  **Dziennik Operacji** na bieżąco informuje o wszystkich krokach: tworzeniu folderów, kopiowaniu i zmianie nazw plików, statusie parsowania oraz ostatecznym utworzeniu pliku `wyniki.xlsx`.
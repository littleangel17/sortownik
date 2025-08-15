# Menedżer Danych Pomiarowych v2.0

## 1. Wprowadzenie

**Menedżer Danych Pomiarowych** to zintegrowane narzędzie 2-w-1, zaprojektowane z myślą o studentach, badaczach i każdej osobie pracującej z dużą liczbą plików pomiarowych. Aplikacja, napisana w języku Python z użyciem biblioteki Tkinter, łączy w sobie dwie kluczowe funkcjonalności: uniwersalny sortownik plików oraz dedykowany analizator danych w formacie `.sit`.

Rozwój aplikacji był wspomagany przez zaawansowany model sztucznej inteligencji **Google Gemini**, co pozwoliło na szybkie zintegrowanie złożonej logiki przetwarzania danych w prostym i intuicyjnym interfejsie graficznym.

## 2. Kluczowe Funkcje

Aplikacja składa się z dwóch niezależnych, ale uzupełniających się modułów:

### Moduł 1: Sortownik Plików
*   **Cel:** Błyskawiczne porządkowanie dowolnego folderu.
*   **Działanie:** Użytkownik wybiera folder, a aplikacja automatycznie skanuje go i przenosi wszystkie pliki do dedykowanych podfolderów, nazwanych zgodnie z ich rozszerzeniami (np. pliki `.pdf` trafiają do folderu `pdf`, a `.jpg` do `jpg`).
*   **Obsługa Plików Bez Rozszerzeń:** Pliki, które nie posiadają formalnego rozszerzenia, są bezpiecznie grupowane w folderze `Pliki_Bez_Rozszerzenia`.
*   **Idempotentność:** Można go uruchamiać wielokrotnie na tym samym folderze bez ryzyka tworzenia duplikatów czy błędów.

### Moduł 2: Analizator Plików `.sit`
*   **Cel:** Przetworzenie surowych danych z plików `.sit`, agregacja i zapis w postaci czytelnego pliku Excel.
*   **Działanie:** Proces jest w pełni zautomatyzowany i przebiega w dwóch etapach:
    1.  **Konwersja (`.sit` -> `.txt`):** Aplikacja rekursywnie przeszukuje wybrany folder, znajduje wszystkie pliki `.sit`, kopiuje je do nowego podfolderu `txt_z_sit`, a następnie zmienia ich rozszerzenie na `.txt`.
    2.  **Analiza i Agregacja (`.txt` -> `.xlsx`):** Następnie, aplikacja automatycznie analizuje dane z nowo utworzonych plików `.txt` w folderze `txt_z_sit`. Każdy plik jest przetwarzany i umieszczany jako osobny, posortowany alfabetycznie arkusz w zbiorczym pliku `wyniki.xlsx`, który jest zapisywany w głównym folderze roboczym.

*   **Graficzny Interfejs Użytkownika:** Prosta i intuicyjna obsługa obu modułów z jednego okna.
*   **Dziennik Operacji:** Wbudowana konsola na bieżąco informuje użytkownika o wszystkich wykonywanych krokach, od tworzenia folderów po status generowania pliku Excel.

## 3. Jak to działa? (Przepływ Pracy)

1.  Użytkownik uruchamia aplikację i klika **"Wybierz Folder"**, aby wskazać katalog roboczy.
2.  Po wybraniu folderu aktywują się dwa przyciski:
    *   **"1. Uporządkuj Pliki w Folderze"**: Uruchamia Moduł 1.
    *   **"2. Przetwórz .sit i Generuj Excel"**: Uruchamia Moduł 2.
3.  Użytkownik wybiera interesującą go operację.
4.  Aplikacja wykonuje zadanie, na bieżąco raportując postępy w **Dzienniku Operacji**.
5.  Po zakończeniu operacji wyświetlany jest komunikat o sukcesie.

## 4. Wymagania i Instalacja

### 4.1. Zależności
Do poprawnego działania aplikacji wymagane są:
- Python 3.x (zalecany 3.8 lub nowszy)
- Tkinter (standardowo dołączany do Pythona; w niektórych dystrybucjach Linuksa może wymagać instalacji, np. `sudo apt-get install python3-tk`)
- Pandas
- Openpyxl (do zapisu plików `.xlsx`)

### 4.2. Instalacja
Otwórz terminal (Wiersz polecenia, PowerShell, Terminal) i zainstaluj wymagane biblioteki za pomocą poniższej komendy:
```bash
pip install pandas openpyxl
```
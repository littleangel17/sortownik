# Sortownik Danych Pomiarowych v1.1

## 1. Wprowadzenie

**Sortownik Danych Pomiarowych** to prosta, ale potężna aplikacja desktopowa napisana w języku Python, wykorzystująca bibliotekę Tkinter. Została stworzona z myślą o studentach i badaczach, zwłaszcza z dziedzin takich jak chemia, fizyka czy biologia. Jej głównym celem jest błyskawiczne uporządkowanie folderów zawierających duże ilości danych pomiarowych z eksperymentów. Rozwój aplikacji był wspomagany przez zaawansowany model sztucznej inteligencji *Google Gemini*.

Aplikacja automatycznie skanuje wskazany folder, identyfikuje pliki o różnych rozszerzeniach (np. `.txt`, `.alt`, `.sit`, `.xls` itd.) i przenosi je do dedykowanych podfolderów, przywracając porządek i znacznie zwiększając efektywność pracy.

## 2. Kluczowe Funkcje

*   **Graficzny Interfejs Użytkownika:** Prosta i intuicyjna obsługa, niewymagająca znajomości linii komend.
*   **Wybór Dowolnego Folderu:** Użytkownik może w łatwy sposób wskazać katalog, który chce uporządkować.
*   **Automatyczne Sortowanie:** Aplikacja sama wykrywa wszystkie unikalne rozszerzenia plików i tworzy dla nich odpowiednie podfoldery (np. `txt`, `alt`, `xls`).
*   **Obsługa Plików Bez Rozszerzeń:** Pliki, które nie posiadają formalnego rozszerzenia, są grupowane w specjalnym folderze `Pliki_Bez_Rozszerzenia`.
*   **Idempotentność:** Program można uruchamiać wielokrotnie na tym samym folderze. Nowe pliki zostaną posortowane do już istniejących podfolderów bez tworzenia duplikatów.
*   **Dziennik Operacji:** Wbudowana konsola na bieżąco informuje użytkownika o postępach: tworzeniu folderów i przenoszeniu każdego pliku.

## 3. Jak to działa? (Zasada działania)

Skrypt wykonuje następujące kroki:
1.  Pobiera listę wszystkich elementów w wybranym folderze.
2.  Iteruje po każdym elemencie, ignorując istniejące podfoldery i przetwarzając tylko pliki.
3.  Dla każdego pliku identyfikuje jego rozszerzenie (np. `.txt`). Nazwa docelowego podfolderu jest tworzona na podstawie tego rozszerzenia, ale bez kropki (`txt`).
4.  Sprawdza, czy podfolder o danej nazwie już istnieje. **Jeśli nie, tworzy go.**
5.  Przenosi plik do odpowiedniego podfolderu.

Dzięki temu podejściu aplikacja jest bezpieczna i efektywna przy wielokrotnym stosowaniu.

## 4. Wymagania i Instalacja

### 4.1. Zależności
Do poprawnego działania aplikacji wymagane są następujące biblioteki:
- Python 3.x (zalecany 3.8 lub nowszy)
- Tkinter (standardowo dołączany do Pythona; w niektórych dystrybucjach Linuksa może wymagać instalacji, np. `sudo apt-get install python3-tk`)
- Pandas

### 4.2. Instalacja
Otwórz terminal (Wiersz polecenia, PowerShell, Terminal) i zainstaluj bibliotekę `pandas` za pomocą poniższej komendy:
```bash
pip install pandas

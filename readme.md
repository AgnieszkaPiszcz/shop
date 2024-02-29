# Sklep internetowy

# Instalacja

Aby uruchomić stronę należy zainstalować sqlite3, Python3.8 lub wyżej oraz zależności pythonowe:

    python3.8 -m pip install -r requirements.txt

Stronę należy uruchomić komendą:

    python3.8 run.py

# Funkcjonalności

Użytkownik niezalogowany może przeglądać kategorie i produkty oraz skorzystać z formularza kontaktowego w zakładce Kontakt. Po rejestracji oraz logowaniu udostępniona jest funkcja dodawania produktów do koszyka oraz składania zamówień. Po zalogowaniu na konto administracyjne adresem email: admin@admin.com oraz hasłem: AdminGromowladny7! można dodawać, edytować i usuwać produkty oraz kategorie.

# Struktura projektu

W pliku routes.py znajdują się poszczególne podstrony, models.py zawiera schemat bazy danych a site.db bazę danych, w forms.py są definicje formularzy. Folder templates zawiera pliki html, natomiast folder static pliki css, js oraz zdjęcia.


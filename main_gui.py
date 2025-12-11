"""
main_gui.py - Einstiegspunkt für die GUI-Version

Startet den Aktivitäten-Planer mit grafischer Oberfläche
"""

from app.controllers.GUIController import GUIController


def main():
    """Hauptfunktion - startet die GUI-Anwendung"""
    try:
        # Controller erstellen und starten
        app = GUIController()
        app.run()

    except Exception as e:
        # Unerwarteter Fehler
        print(f"\n!!! Ein Fehler ist aufgetreten: {e} !!!")
        print("Bitte überprüfe deine .env Datei und Internetverbindung.")
        print("Stelle sicher, dass tkinter installiert ist.")


if __name__ == "__main__":
    main()
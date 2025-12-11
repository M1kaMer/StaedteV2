"""
Controller für GUI-Version
Koordiniert zwischen Model und GUI-View
"""

from app.models.TripData import TripData
from app.models.GeminiService import GeminiService
from app.views.GUIView import GUIView


class GUIController:
    """
    GUI Controller - koordiniert den Ablauf für die GUI-Version
    """

    def __init__(self):
        # Model initialisieren
        self.data = TripData()
        self.ai_service = GeminiService()

        # View initialisieren mit Model-Referenz
        self.view = GUIView(self.data)

        # Callback für Start-Button setzen
        self.view.set_start_callback(self.handle_start_request)

    def run(self):
        """Startet die GUI"""
        self.view.run()

    def handle_start_request(self):
        """
        Wird aufgerufen wenn der Benutzer auf Start klickt
        Behandelt den kompletten Ablauf
        """
        # Stadt-Eingabe holen und validieren
        city = self.view.get_city_input()

        if not self.data.is_city_valid(city):
            self.view.show_error("Bitte gib einen gültigen Ausflugsort ein!")
            return

        # Stadt speichern
        self.data.set_city(city)

        # Vibe holen und speichern
        vibe_choice = self.view.get_vibe_input()
        if not self.data.set_vibe_from_choice(vibe_choice):
            self.view.show_error("Ungültige Vibe-Auswahl!")
            return

        # Loading anzeigen
        self.view.show_loading()

        try:
            # AI-Empfehlungen holen
            recommendations = self.ai_service.fetch_suggestions(
                self.data.city,
                self.data.vibe
            )

            # Im Model speichern
            self.data.set_recommendations(recommendations)

            # Ergebnisse anzeigen (View holt Daten aus Model)
            self.view.show_results()

        except Exception as e:
            self.view.show_error(f"Fehler beim Laden der Empfehlungen: {e}")
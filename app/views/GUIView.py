"""
View - GUI mit Tkinter
Alternative View-Implementierung zur ConsoleView
Liest Daten direkt aus dem Model für die Darstellung
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class GUIView:
    """View für GUI-basierte Interaktion mit Tkinter"""

    def __init__(self, model):
        """
        Initialisiert GUI View mit Referenz zum Model

        Args:
            model: TripData Instanz
        """
        self.model = model
        self.window = tk.Tk()
        self.window.title("Aktivitäten-Planer")
        self.window.geometry("600x500")

        # Callback für Controller (wird später gesetzt)
        self.on_start_callback = None

        self._setup_ui()

    def _setup_ui(self):
        """Erstellt die UI-Elemente"""
        # Überschrift
        title_label = tk.Label(
            self.window,
            text="🎯 Aktivitäten-PLANER",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=20)

        # Input-Frame
        input_frame = ttk.Frame(self.window, padding="10")
        input_frame.pack(fill="x", padx=20)

        # Stadt-Input
        ttk.Label(input_frame, text="Ausflugsort:", font=("Arial", 11)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.city_entry = ttk.Entry(input_frame, width=30, font=("Arial", 11))
        self.city_entry.grid(row=0, column=1, pady=5, padx=10)

        # Vibe-Auswahl
        ttk.Label(input_frame, text="Stimmung:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.vibe_var = tk.StringVar(value="Action")
        vibe_frame = ttk.Frame(input_frame)
        vibe_frame.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        ttk.Radiobutton(
            vibe_frame,
            text="Action & Abenteuer",
            variable=self.vibe_var,
            value="Action"
        ).pack(side="left", padx=5)

        ttk.Radiobutton(
            vibe_frame,
            text="Ruhe & Entspannung",
            variable=self.vibe_var,
            value="Entspannung"
        ).pack(side="left", padx=5)

        # Start-Button
        self.start_button = ttk.Button(
            self.window,
            text="Empfehlungen holen",
            command=self._on_start_clicked
        )
        self.start_button.pack(pady=20)

        # Ergebnis-Textfeld
        result_frame = ttk.LabelFrame(
            self.window,
            text="Empfehlungen",
            padding="10"
        )
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=("Arial", 10),
            state="disabled"
        )
        self.result_text.pack(fill="both", expand=True)

        # Status-Label
        self.status_label = tk.Label(
            self.window,
            text="Bereit",
            font=("Arial", 9),
            fg="gray"
        )
        self.status_label.pack(pady=5)

    def set_start_callback(self, callback):
        """
        Setzt den Callback für den Start-Button

        Args:
            callback: Funktion die aufgerufen wird (Controller-Methode)
        """
        self.on_start_callback = callback

    def _on_start_clicked(self):
        """Wird aufgerufen wenn Start-Button geklickt wird"""
        if self.on_start_callback:
            self.on_start_callback()

    def get_city_input(self) -> str:
        """Holt Stadt-Eingabe vom Benutzer"""
        return self.city_entry.get().strip()

    def get_vibe_input(self) -> str:
        """Holt Stimmungs-Auswahl vom Benutzer"""
        return self.vibe_var.get()

    def show_loading(self):
        """Zeigt Ladeanzeige"""
        self.status_label.config(text="⏳ Lädt Empfehlungen...", fg="blue")
        self.start_button.config(state="disabled")
        self.window.update()

    def show_results(self):
        """
        Zeigt Ergebnisse an - holt Daten direkt aus dem Model
        """
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)

        # Überschrift
        self.result_text.insert(tk.END, f"📍 Tipps für {self.model.city}\n\n", "title")

        # Empfehlungen
        self.result_text.insert(tk.END, self.model.recommendations)

        # Styling für Titel
        self.result_text.tag_config("title", font=("Arial", 12, "bold"))

        self.result_text.config(state="disabled")

        # Status aktualisieren
        self.status_label.config(text="✅ Empfehlungen geladen", fg="green")
        self.start_button.config(state="normal")

    def show_error(self, message: str):
        """Zeigt Fehlermeldung"""
        messagebox.showerror("Fehler", message)
        self.status_label.config(text="❌ Fehler aufgetreten", fg="red")
        self.start_button.config(state="normal")

    def show_welcome(self):
        """Zeigt Willkommensnachricht (bei GUI nicht nötig)"""
        pass

    def show_goodbye(self):
        """Zeigt Abschiedsnachricht und schließt Fenster"""
        messagebox.showinfo("Auf Wiedersehen", "Bis zum nächsten Mal!")
        self.window.quit()

    def run(self):
        """Startet die GUI Event-Loop"""
        self.window.mainloop()
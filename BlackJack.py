# Importieren des Tkinter für das Graphic Interface
from tkinter import *
# ttk für Buttons importieren (wegen Mac-Bug, siehe https://stackoverflow.com/questions/52529403/button-text-of-tkinter-does-not-work-in-mojave)
from tkinter import ttk 
# Import random für das zufällige Ziehen von Spielkarten
import random
# Import datetime für die Ausgabe der aktuellen Zeit des Statistik-Exports
import datetime

# Definition des Designs für das GUI Fenster
master = Tk()
master.geometry("500x570")
master.title("BlackJack – by Lukas und Nicolas")

# Readme.txt importieren zur Anzeige in der Konsole
readme = open("Readme.txt", "r")
print(readme.read())

class Deck:
    
    """
    Das Deck beinhaltet die Spielkarten und wird genutzt, um zufällige Karten auszugeben.
    Die Keys beschreiben die Karten, während die Values jeweils den entsprechenden Wert beinhalten.
    """
    
    dict_deck = {}
    dict_deck_counter = {}
    
    
    def get_card(self):
        
        """
        Die Funktion holt zufällige Karten aus dem Deck und gibt deren Anzeige und Wert zurück. 
        """
      
        card = random.choice(list(self.dict_deck.keys()))
        value = deck.dict_deck[card]
        # Funktion zum Entfernen der gezogenen Karte aufrufen
        self.remove_card(card)
        return card, value
        
        
    def remove_card(self, card):
        """
        Die Funktion sorgt dafür, dass jede Karte nur maximal 4 Mal pro Runde gezogen werden kann. 
        """
        self.dict_deck_counter[card] -= 1
        # Wenn eine Karte 4 Mal ausgespielt wurde, wird sie aus dem Deck entfernt
        if self.dict_deck_counter[card] == 0:
            del self.dict_deck[card]
            
    def reset_deck(self):
        
        """
        Die Funktion dient dazu, das Kartedeck sowie den Kartenzähler für jede neue Runde zurückzusetzen. 
        """
      
        self.dict_deck = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.dict_deck_counter = {'2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, '10': 4, 'J': 4, 'Q': 4, 'K': 4, 'A': 4}
    
        
deck = Deck()


class Statistik:
    
    """
    Die Statistik wird während der ganzen Spielverlaufs geführt. Sobald jemand gewinnt, erhält derjenige einen Punkt. 
    """
  
    stat_player = 0
    stat_dealer = 0
    stat_unentschieden = 0
    
    def winner(self, winner):
        """
        Die Funktion wird dazu verwendet, dem jeweiligen Gewinner einen Punkt zuzuschreiben.
        """
        if winner == "player":
            self.stat_player += 1
            lbl_win_player.config(text="Player: " + str(self.stat_player))
        
        elif winner == "dealer":
            self.stat_dealer += 1
            lbl_win_dealer.config(text="Dealer: " + str(self.stat_dealer))
            
        else:
            self.stat_unentschieden += 1
            lbl_win_win.config(text="Unentschieden: " + str(self.stat_unentschieden))
        
statistik = Statistik()


class Player:
    card_1_player = 0
    card_2_player = 0
    hit_list = []
    summe_player = 0
    
    
    def play(self):
        """
        Die Funktion dient dazu, die Runde seitens des Spielers zu eröffnen.
        Es werden dabei zufällig zwei Karten gezogen und im GUI angezeigt.
        """
        self.card_1_player = deck.get_card()
        self.card_2_player = deck.get_card()
        self.summe_player = self.card_1_player[1] + self.card_2_player[1]
        
        # Spieler-Karten im GUI anzeigen
        lbl_card1_player.config(text="1. Karte: " + str(player.card_1_player[0]))
        lbl_card2_player.config(text="2. Karte: " + str(player.card_2_player[0]))
        
        # Summe im GUI anzeigen
        lbl_sum_player.config(text="Summe: " + str(self.summe_player))
        
        #Summe prüfen
        self.check_player_cards()
        
           
        
    def hit(self):
        """
        Die Funktion dient dazu, dass der Spieler weitere Karten ziehen kann (Hit). 
        """
        card_hit = deck.get_card()
        self.hit_list.append(card_hit[0])
        self.summe_player += card_hit[1]

        # Liste mit weiteren Karten zur Anzeige in String umwandeln
        str_hit_list = (', '.join([str(elem) for elem in self.hit_list]))
        
        # Liste (bzw. String) mit weiteren Karten im GUI anzeigen
        lbl_card_hit1.config(text="Weitere Karten: " + str((str_hit_list)))
        
        #Summe im GUI anzeigen
        lbl_sum_player.config(text="Summe: " + str(self.summe_player))
        
        #Summe des Spielers prüfen
        self.check_player_cards()
        
        
    def check_player_cards(self):
        """
        Die Funktion wird dazu verwendet, die Summe des Spielers während seines Zuges zu prüfen. 
        Hat der Spieler 21 Punkte, gewinnt er sofort mit BLACKJACK. 
        Wenn der Spieler überbietet (> 21), verliert er sofort. 
        """
        if self.summe_player == 21:
            lbl_warning.config(bg="green", fg="white", text="Du hast BLACKJACK und gewinnst!")
        
            # Spieler erhält einen Punkt
            statistik.winner("player")
        
            # Buttons konfigurieren
            button_config("start")
        
        elif self.summe_player > 21:
            lbl_warning.config(bg="red", fg="white", text="Du hast überboten und verlierst!")
            
            # Spieler erhält einen Punkt
            statistik.winner("dealer")
            
            # Buttons konfigurieren
            button_config("start")
        
        else:
            pass

        
    def reset_cards(self):
        """
        Funktion zum Resetten der vorhergehenden Runde (Player)
        """
        # Liste mit weiteren Karten leeren
        self.hit_list = []
        # Weitere Karten im GUI entfernen
        lbl_card_hit1.config(text="Weitere Karten: ")
        
    
        
player = Player()
    
        
class Dealer:
    card_1_dealer = 0
    card_2_dealer = 0
    hit_list = []
    summe_dealer = 0
    
    def play(self):
        """
        Die Funktion dient dazu, die Runde seitens des Dealers zu eröffnen.
        Es werden dabei zufällig zwei Karten gezogen. Es wird anfangs nur die erste Karte angezeigt. 
        """
        self.card_1_dealer = deck.get_card()
        self.card_2_dealer = deck.get_card()
        self.summe_dealer = self.card_1_dealer[1] + self.card_2_dealer[1]
        
        # Anzeigen der Dealer Karten im GUI (2. Karte bleibt verdeckt)
        lbl_card1_dealer.config(text="1. Karte: " + str(dealer.card_1_dealer[0]))
        lbl_card2_dealer.config(text="2. Karte: verdeckt")
        
    def reset_cards(self):
        """
        Funktion zum Resetten der vorhergehenden Runde (Dealer)
        """
        # Liste mit weiteren Karten leeren
        self.hit_list = []
        # Weitere Karten und Summe im GUI entfernen
        lbl_card_hit_dealer.config(text="Weitere Karten: ")
        lbl_sum_dealer.config(text="Summe: ")
        
        
    def stand(self):
        """
        Die Funktion wird ausgeführt, sobald der Player auf 'Stand' drückt. 
        Dadurch ist der Dealer an der Reihe. Dieser zieht solange Karten, bis seine Summe > 17 ist.
        """
        lbl_card2_dealer.config(text="2. Karte: " + str(self.card_2_dealer[0]))
        
        while self.summe_dealer < 17:
            card_hit = deck.get_card()
            self.hit_list.append(card_hit[0])
            self.summe_dealer += card_hit[1]
            
            # Liste mit weiteren Karten zur Anzeige in String umwandeln
            str_hit_list = (', '.join([str(elem) for elem in self.hit_list]))
            # Liste (bzw. String) mit weiteren Karten im GUI anzeigen
            lbl_card_hit_dealer.config(text="Weitere Karten: " + str((str_hit_list)))
            
        #Summe anzeigen
        lbl_sum_dealer.config(text="Summe: " + str(self.summe_dealer))
    
        # Dealer Summe prüfen
        self.check_dealer_cards()
        
        
    def check_dealer_cards(self):
        """
        Die Funktion wird dazu verwendet, die Summe des Dealers während seines Zuges zu prüfen. 
        Hat der Dealer 21 Punkte, gewinnt er sofort mit BLACKJACK. 
        Wenn der Dealer überbietet (> 21), verliert er sofort. 
        """
        if self.summe_dealer > 21:
            lbl_warning.config(bg="green", fg="white", text="Der Dealer hat überboten. Du gewinnst!")
        
            # Spieler erhält einen Punkt
            statistik.winner("player")
        
            # Buttons konfigurieren
            button_config("start")
        
        elif self.summe_dealer == 21:
            lbl_warning.config(bg="red", fg="white", text="Der Dealer hat BLACKJACK. Du verlierst!")
            
            # Spieler erhält einen Punkt
            statistik.winner("dealer")
            
            # Buttons konfigurieren
            button_config("start")

        # Wenn der Dealer nach Zug seiner weiteren Karten eine Summe zwischen 17 und 20 erreicht, geht das Spiel in den Endvergleich.   
        else:
            end_game(player.summe_player, dealer.summe_dealer)
                
dealer = Dealer()

def end_game(summe_player, summe_dealer):
    """
    Die Funktion vergleich am Ende des Spiels die Summen von Player und Dealer.
    Derjenige mit der höheren Summe gewinnt und erhält einen Punkt. 
    """
    if summe_dealer < summe_player:
        lbl_warning.config(bg="green", fg="white", text="Du gewinnst mit " + str(summe_player) + " Punkten gegen den Dealer mit " + str(summe_dealer) + " Punkten!")
        
        # Spieler erhält einen Punkt
        statistik.winner("player")
        
        # Buttons konfigurieren
        button_config("start")
    
    elif summe_dealer == summe_player:
        lbl_warning.config(bg="orange", fg="white", text="Es ist mit " + str(summe_player) + " zu " + str(summe_dealer) + " Punkten unentschieden!")
        
        # Es wird eine Runde als unentschieden gezählt
        statistik.winner("unentschieden")
        
        # Buttons konfigurieren
        button_config("start")
        
    else:
        lbl_warning.config(bg="red", fg="white", text="Du verlierst mit " + str(summe_player) + " Punkten gegen den Dealer mit " + str(summe_dealer) + " Punkten!")
        
        # Dealer erhält einen Punkt
        statistik.winner("dealer")
        
        # Buttons konfigurieren
        button_config("start")
        

def button_config(state):
    """
    Die Funktion definiert den Status der Buttons während des Spielverlaufs. 
    """
    # wenn das Spiel läuft, sind nur die Button 'Hit' und 'Stand' aktiviert. 
    if state == "playing":
        btn_hit.config(state=NORMAL)
        btn_stand.config(state=NORMAL)
        btn_play.config(text="Neue Runde", state=DISABLED)
    # wenn gerade keinde Runde läuft, ist nur der 'Play'-Button aktiv
    else:
        btn_hit.config(state=DISABLED)
        btn_stand.config(state=DISABLED)
        btn_play.config(state=NORMAL)
        

def start_game():
    """
    Die Funktion wird ausgeführt durch den User-Klick auf "Spiel beginnen" bzw. "Neue Runde". Das Spiel wird dadurch gestartet oder eine neue Runde beginnt.
    Hierbei werden zuerst  alle Variablen zurückgesetzt (Funktionen 'reset_cards').
    Die ersten Handkarten (2 für den Spieler, 2 für den Dealer) werden zufällig verteilt.
    """

    # Aufruf reset-Funktion
    lbl_warning.config(bg="white",text="")
    deck.reset_deck()
    player.reset_cards()
    dealer.reset_cards()
    
    #Spiel startet. Erste Karten werden verteilt. 
    player.play()
    dealer.play()
    
    # Buttons konfigurieren
    button_config("playing")


def export():
    """Die Funktion exportiert die aktuelle Statistik inklusive Zeitstempel in ein txt-File."""

    now = datetime.datetime.now()
    with open("Statistik_BlackJack.txt", "a") as open_file:
        open_file.write("\n\nDatum und Zeit: " + str(now.strftime("%d.%m.%Y %H:%M:%S"))
                        + "\nPlayer: " + str(statistik.stat_player)
                        + "\nDealer: " + str(statistik.stat_dealer)
                        + "\nUnentschieden: " + str(statistik.stat_unentschieden)) 
    

def destroy():
    """
    Die Funktion wird ausgeführt durch User-Klick auf "Exit".
    Dadurch wird das GUI geschlossen und der Code gestoppt. 
    """
    master.destroy()
    
 
 
"""Ab hier wird das Layout mithilfe des Tkinter-Moduls definiert"""
    
# Play-Button (Spiel beginnen)

btn_play = ttk.Button(master, text="Spiel beginnen", command=start_game)
btn_play.pack(pady=5)

# Section Player

Label(text="PLAYER", font="Helvetica 12 bold").pack()

lbl_card1_player = Label(master, text="1. Karte: ")
lbl_card1_player.pack()

lbl_card2_player = Label(master, text="2. Karte: ")
lbl_card2_player.pack()

lbl_card_hit1 = Label(master, text="Weitere Karten: ")
lbl_card_hit1.pack()

lbl_sum_player = Label(master, text="Summe: ")
lbl_sum_player.pack()


# Buttons für die Spielsteuerung (Hit und Stand)

btn_frame = Frame(master, height=100)
btn_frame.pack(pady=10)

btn_hit = ttk.Button(btn_frame, text="Hit", state=DISABLED, command=player.hit)
btn_hit.grid(row=0, column=0)

btn_stand = ttk.Button(btn_frame, text="Stand", state=DISABLED, command=dealer.stand)
btn_stand.grid(row=0, column=1)


# Section Dealer

Label(text="DEALER", font="Helvetica 12 bold").pack()

lbl_card1_dealer = Label(master, text="1. Karte: ")
lbl_card1_dealer.pack()

lbl_card2_dealer = Label(master, text="2. Karte: ")
lbl_card2_dealer.pack()

lbl_card_hit_dealer = Label(master, text="Weitere Karten: ")
lbl_card_hit_dealer.pack()

lbl_sum_dealer = Label(master, text="Summe: ")
lbl_sum_dealer.pack()


# Meldungen über Spielereignisse (Veloren, Blackjack, etc.)

lbl_warning = Label(master)
lbl_warning.pack(pady=10)


# Section Statistik

Label(text="STATISTIK", font="Helvetica 12 bold").pack()

Label(text="Gewonnene Runden", font="Helvetica 12 bold").pack()
lbl_win_player = Label(master, text="Player: 0")
lbl_win_player.pack()
lbl_win_dealer = Label(master, text="Dealer: 0")
lbl_win_dealer.pack()
lbl_win_win = Label(master, text="Unentschieden: 0")
lbl_win_win.pack()


# Statistik exportieren

btn_end = ttk.Button(master, text="Statistik exportieren", command=export)
btn_end.pack(pady=10)


# Button zum Beenden des Spiels / Schliessen des Fensters (Exit)

btn_end = ttk.Button(master, text="Exit", command=destroy)
btn_end.pack(pady=10)


# Ausführen des Tkinter GUIs

master.mainloop()
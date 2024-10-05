import machine
import utime
from SimplyServos import KitronikSimplyServos

servos = KitronikSimplyServos(1)

bouton_reset = machine.Pin(machine.Pin(26), machine.Pin.IN, machine.Pin.PULL_DOWN)
boutonDown = machine.Pin(machine.Pin(27), machine.Pin.IN, machine.Pin.PULL_DOWN)
boutonUp = machine.Pin(machine.Pin(28), machine.Pin.IN, machine.Pin.PULL_DOWN)

position_servo = 100  # Position initiale du servomoteur (30 degrés)
dernier_etat_boutonUp = False
dernier_etat_boutonDown = False
etat_relay = False
limite_inferieure = 90
limite_superieure = 125

# Définir la position initiale du servomoteur
servos.goToPosition(0, position_servo)
utime.sleep_ms(1000)  # Attendre 1 seconde pour que le servomoteur atteigne la position initiale

while True:
    etat_boutonUp = boutonUp.value()
    etat_boutonDown = boutonDown.value()
    etat_relay_bouton = bouton_reset.value()
    
    print("État du bouton Up :", etat_boutonUp)  # Afficher l'état du bouton Up
    print("État du bouton Down :", etat_boutonDown)  # Afficher l'état du bouton Down
    
    if etat_boutonDown and not dernier_etat_boutonDown:
        if position_servo - 5 >= limite_inferieure:
            position_servo -= 5
        print("Position du servomoteur :", position_servo)  # Afficher la position du servomoteur
        servos.goToPosition(0, position_servo)
        utime.sleep_ms(10)

    if etat_boutonUp and not dernier_etat_boutonUp:
        if position_servo + 5 <= limite_superieure:
            position_servo += 5
        print("Position du servomoteur :", position_servo)  # Afficher la position du servomoteur
        servos.goToPosition(0, position_servo)
        utime.sleep_ms(10)
        
    print("État du bouton :", etat_relay_bouton)  # Afficher l'état du bouton
    if etat_relay_bouton and not etat_relay:
        position_servo = 100  # Réinitialiser la position du servomoteur à la position initiale
        servos.goToPosition(0, position_servo)
        print("RESET ON")  # Afficher un message lorsque le relay est activé
        print("Position du servomoteur :", position_servo)
        utime.sleep_ms(1000)
    elif not etat_relay_bouton and etat_relay:
        print("RESET OFF")  # Afficher un message lorsque le relay est désactivé
    utime.sleep_ms(10)  # ajoutez un court délai pour éviter les basculements rapides
    
    dernier_etat_boutonUp = etat_boutonUp
    dernier_etat_boutonDown = etat_boutonDown

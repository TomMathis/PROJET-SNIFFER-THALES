




import struct
import datetime
from datetime import datetime, timedelta

# connexion à la BDD Mysql et insertion du nom de fichier et la datetime
import mysql.connector
from datetime import datetime

# connexion avec le dictionnaire
from dic import FT_0
from dic import MAC
from dic import IP
from dic import FT_1
from dic import FT_2
from dic import FT_3
from dic import FT_4
from dic import FT_5
from dic import FT_6
from dic import FT_7

#on demande les 2 fichiers
nomfic=input("donne le nom du fichier trame : " )

nomfic2=input("donne le nom du .rep : " )

#fonction pour trouver la date d'execution
def trouver_date(nomfic2):
    mot_cle = "Execution begin date"
    mot_suivant = ""

    with open(nomfic2, 'r') as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            if mot_cle in ligne:
                index = ligne.index(":")
                mot_suivant = ligne[index+1:].strip().strip('"')
                break

    if mot_suivant:
        mot_suivant = "20" + mot_suivant
        parties = mot_suivant.split(" ")
        deuxieme_partie = parties[1].replace("-", ":")
        resultat = parties[0] + " " + deuxieme_partie
        return resultat



#fonction pour trouver le nom du fichier
def rechercher_nom(nomfic2):
    with open(nomfic2, 'r') as file:
        lines = file.readlines()

        for line in lines:
            words = line.strip().split()
            for i in range(len(words) - 1):
                if words[i] == "Test" and words[i+1] == ":":
                    if i + 2 < len(words):
                        result = ' '.join(words[i+2:])
                        return result
                    

# Définir les valeurs à insérer
nomfichier=rechercher_nom(nomfic2)
valeur_date_heure=trouver_date(nomfic2)
values = (nomfichier, valeur_date_heure)



#VERIF EXISITANTE FICHIER SUIVANT LA DATE D EXECUTION

# Connexion à la base de données
conn2 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ft",
    ssl_disabled=True
)
cursor2 = conn2.cursor()

# Requête SQL avec un paramètre pour la valeur de la date/heure
sql_verif_date_execution = "SELECT DateTime FROM transfert WHERE DateTime = %s"

# Exécution de la requête SQL avec le paramètre
cursor2.execute(sql_verif_date_execution, (valeur_date_heure,))
result = cursor2.fetchall()

# Fermeture de la connexion à la base de données
cursor2.close()
conn2.close()
# Vérification du résultat
if result:
  print("La valeur de date/heure existe deja dans la table : ", valeur_date_heure , " veuillez sélectionner un autre fichier.")
else:
    
  # Se connecter à la base de données
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ft",
    ssl_disabled=True
  )

  # Créer un curseur
  mycursor = mydb.cursor()

  # Définir la requête SQL
  sql = "INSERT INTO transfert (nomfichier, datetime) VALUES (%s, %s)"
  # Exécuter la requête avec les valeurs

  mycursor.execute(sql, values)

  # Valider les changements dans la base de données
  mydb.commit()


  



  # fonction pour mettre l'adresse MAC dans la bonne forme
  def formater_adresse_mac(adresse_mac):
    adresse_mac_formatee = ""
    blocs = adresse_mac.split(
      ":")  # On divise l'adresse en blocs séparés par des ":"
    for bloc in blocs:
      if len(bloc) == 1:  # Si le bloc ne contient qu'un seul chiffre
        adresse_mac_formatee += "0" + bloc + ":"  # On rajoute un 0 avant le chiffre et le bloc est terminé par un ":"
      else:
        adresse_mac_formatee += bloc + ":"  # Sinon, on ajoute simplement le bloc et un ":"
    adresse_mac_formatee = adresse_mac_formatee[:
                                                -1]  # On retire le dernier ":" ajouté
    return adresse_mac_formatee


  # fonction pour traduire en suivant le format ieee754
  def ieee754_double(octets):
    binaire = ''.join(f'{octet:08b}' for octet in octets)
    signe = -1 if binaire[0] == '1' else 1
    exposant = int(binaire[1:12], 2) - 1023
    mantisse = 1 + int(binaire[12:], 2) / 2**52
    return signe * mantisse * 2**exposant

  # traduction des secondes en une date au format jour/mois/annee heure/minute/seconde
  def secondes_vers_date(secs):
    dt = datetime.fromtimestamp(secs)
    millisecondes = int((secs - int(secs)) * 1000)
    return dt.strftime("%d/%m/%Y %H:%M:%S") + "," + str(millisecondes).zfill(3)

  # donne les nombres d'octets pour n bits
  def nboctets(a):
    return (a / 8)

  # donne le nombre de bits pour n octets
  def nbbits(a):
    return (a * 8)

  # transforme le decimal en hexadecimal
  def decimal_vers_hexadecimal(decimal):
    hexadecimal = hex(decimal)
    if len(hexadecimal) == 3:
      hexa2 = hexadecimal
      hexadecimal = ""
      hexadecimal += hexa2[0] + hexa2[1] + "0" + hexa2[2]
    return hexadecimal

  # focntion qui prend une liste , la transforme en binaire, fusion les bianires cote a cote et qui en renvoye le decimal
  def listebinaire_vers_decimal(liste):
    binaires = []
    for nombre in liste:
      binaire = ""
      quotient = nombre
      while quotient > 0:
        reste = quotient % 2
        binaire = str(reste) + binaire
        quotient = quotient // 2
      while len(binaire) < 8:
        binaire = "0" + binaire
      binaires.append(binaire)
    binaire_complet = ''.join(binaires)
    decimal = 0
    for i in range(len(binaire_complet)):
      decimal += int(binaire_complet[i]) * (2**(len(binaire_complet) - i - 1))

    return decimal

  # donne les positions
  def get_padding_length(position):
    # Déterminer la longueur du padding en fonction de la position
    if position == 0:
      return 1
    elif position == 1:
      return 5
    elif position == 2 or position == 3:
      return 6
    elif position == 4:
      return 10
    else:
      return 0  # Gérer les positions non définies

  # focntion qui convertit une liste de decimaux en hexadecimaux
  def convert_decimals_to_hexadecimal(input_list):
    binary_string = ""

    # Convertir chaque nombre décimal en binaire
    for i, number in enumerate(input_list):
      binary_number = bin(number)[2:]  # Convertir en binaire
      padding_length = get_padding_length(i)  # Obtenir la longueur du padding
      padded_binary_number = binary_number.zfill(
        padding_length)  # Ajouter le padding
      binary_string += padded_binary_number

    # Diviser le binaire en paquets de 4 bits
    binary_chunks = [
      binary_string[i:i + 4] for i in range(0, len(binary_string), 4)
    ]

    # Convertir chaque paquet binaire en hexadécimal
    hexadecimal_string = ""
    for binary_chunk in binary_chunks:
      hexadecimal_digit = hex(int(binary_chunk,
                                  2))[2:]  # Convertir en hexadécimal
      hexadecimal_string += hexadecimal_digit

    return hexadecimal_string

  # transforme un binaire en decimal
  def binaire_vers_decimal(binaire):
    decimal = 0
    for i in range(len(binaire)):
      if binaire[i] == '1':
        decimal += 2**(len(binaire) - i - 1)
    return decimal

  # transforme une liste d'octets en binaire
  def listeoctets_vers_binaire(octets):
    binaires = []
    for octet in octets:
      binaire = ""
      quotient = octet
      while quotient > 0:
        reste = quotient % 2
        binaire = str(reste) + binaire
        quotient = quotient // 2
      while len(binaire) < 8:
        binaire = "0" + binaire
      binaires.append(binaire)
    binaire_complet = ''.join(binaires)
    return binaire_complet

  # transforme un octet en binaire
  def octet_to_binaire(octet):
    binaire = ""
    for i in range(8):
      bit = octet % 2
      octet = octet // 2
      binaire = str(bit) + binaire
    return binaire

  # fusionne une liste de decimaux
  def fusion_decimal(liste):
    binaires = [octet_to_binaire(octet) for octet in liste]
    binaire = "".join(binaires)

    trad = binaire_vers_decimal(binaire)

    return trad

  # fonction qui coupe le fichier trame ethernet en plusieurs liste qui comporte chacune une trame
  def couper(a, compteur, compteur2):
    l = []
    for i in range(compteur, compteur2):
      l.append(a[i])
    b = fusion_decimal(l)
    b += 28 # car on doit ajouter 28 pour taille trame
    return (b)

  # donne le type 800 ou 806 de la trame
  def type(liste):
    l = []
    l2 = []
    for x in range(40, 42):
      l.append(liste[x])
    a = listebinaire_vers_decimal(l)
    a = decimal_vers_hexadecimal(a)
    l2.append(a)
    l2 = str(l2[0])
    if l2 == "0x800":
      return "800"
    elif l2 == "0x806":
      return "806"


  # FONCTION PRINCIPALE
  def sniffeur(nomfic):
    #ouverture du fichier
    with open(nomfic, 'rb') as f:

      bytes_list = list(f.read())
      compteur = 24 # debut emplacement taille
      compteur2 = 28 # fin emplacement taille
      listecomplete = []
      listecompletetraduite = []

      taillefichier = 0

      # cette partie sert a couper le fichier en liste de liste avec les trames
      while taillefichier < (len(bytes_list)):
        coup = couper(bytes_list, compteur, compteur2)

        listedemi = []

        for i in range(taillefichier, taillefichier + coup):
          listedemi.append(bytes_list[i])
        taillefichier += coup
        listecomplete.append(listedemi)
        compteur += coup
        compteur2 += coup

      # traduction trame 806
      for i in range(len(listecomplete)):
        #on definit toutes les variables de la trame 806
        if type(listecomplete[i]) == "806":
          bench_1_806 = []
          Frame_Date_806 = []
          bench_3_806 = []
          bench_4vide_806 = []
          bench_4_806 = []
          bench_5_806 = []
          bench_6_806 = []
          Frame_Size_806 = []
          MAC_Dest_806 = []
          MAC_Source_806 = []
          field_1_806 = []
          field_2_806 = []
          field_3_806 = []
          field_4_806 = []
          field_5_806 = []
          field_6_806 = []
          MAC_Sender_806 = []
          Sender_IP_806 = []
          MAC_Target_806 = []
          Target_IP_806 = []
          # on regarde avec l'emplacement dans la liste de quel champs de la trame cela correspond
          for y in range(len(listecomplete[i])):

            if y == 0:

              # on traduit donc le champs en fonction de ce que c'est ( decimal , adresse IP, adresse MAC, date ...)
              
              l = []
              for x in range(0, 8):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              bench_1_806.append(a)
              bench_1_806 = str(bench_1[0])

            if y == 8:

              l = []
              for x in range(8, 16):
                l.append(listecomplete[i][x])
              a = l
              Frame_Date_806 = a
              nombre_secondes = ieee754_double(Frame_Date_806)
              date = secondes_vers_date(nombre_secondes)
              Frame_Date_806 = date

            if y == 16:

              l = []
              for x in range(16, 20):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              bench_3_806.append(a)
              bench_3_806 = str(bench_3_806[0])

            if y == 20:
              for x in range(20, 24):
                bench_4vide_806.append(listecomplete[i][x])
              a = listeoctets_vers_binaire(bench_4vide_806)
              for ab in range(len(a)):
                if 0 <= ab <= 11:
                  bench_4_806.append(a[ab])
                elif 12 <= ab <= 15:
                  bench_5_806.append(a[ab])
                else:
                  bench_6_806.append(a[ab])
              # la partie qui suit sert a connecter le resultat au dictionnaire et si il y a correspondance on associe (transfert)
              bench_4_bis_806 = []
              bench_4_bis_806.append(binaire_vers_decimal(bench_4_806))
              bench_4_806 = bench_4_bis_806
              bench_5_bis_806 = []
              bench_5_bis_806.append(binaire_vers_decimal(bench_5_806))
              bench_5_806 = bench_5_bis_806[0]
              bench_5_806 = str(bench_5_806)
              bench_5_trad_806 = bench_5_806
              if bench_5_trad_806 in FT_0.keys():
                transfert = FT_0[bench_5_trad_806]
                bench_5_806 += " " + transfert
              bench_6_bis_806 = []
              bench_6_bis_806.append(binaire_vers_decimal(bench_6_806))
              bench_6_806 = bench_6_bis_806

            if y == 24:
              l = []
              for x in range(24, 28):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              Frame_Size_806.append(a)
              Frame_Size_806 = str(Frame_Size_806[0])

            if y == 28:
              l = []
              for x in range(28, 34):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                # ici on gere adresse MAC + transfert
                MAC_Dest_806.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Dest_806])
              MAC_Dest_806 = resultat
              MAC_Dest_trad_806 = formater_adresse_mac(MAC_Dest_806)
              if MAC_Dest_trad_806 in MAC.keys():
                transfert = MAC[MAC_Dest_trad_806]
                MAC_Dest_trad_806 += " "
                MAC_Dest_trad_806 += transfert
                MAC_Dest_806 = MAC_Dest_trad_806

            if y == 34:
              l = []
              for x in range(34, 40):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                MAC_Source_806.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Source_806])
              MAC_Source_806 = resultat
              MAC_Source_trad_806 = formater_adresse_mac(MAC_Source_806)
              if MAC_Source_trad_806 in MAC.keys():
                transfert = MAC[MAC_Source_trad_806]
                MAC_Source_trad_806 += " "
                MAC_Source_trad_806 += transfert
                MAC_Source_806 = MAC_Source_trad_806

            if y == 40:

              l = []
              for x in range(40, 42):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              a = decimal_vers_hexadecimal(a)
              field_1_806.append(a)
              field_1_806 = str(field_1_806[0])

            if y == 42:

              l = []
              for x in range(42, 44):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_2_806.append(a)
              field_2_806 = str(field_2_806[0])

            if y == 44:

              l = []
              for x in range(44, 46):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_3_806.append(a)
              field_3_806 = str(field_3_806[0])

            if y == 46:

              l = []
              l.append(listecomplete[i][46])
              a = listebinaire_vers_decimal(l)
              field_4_806.append(a)
              field_4_806 = str(field_4_806[0])

            if y == 47:

              l = []
              l.append(listecomplete[i][47])
              a = listebinaire_vers_decimal(l)
              field_5_806.append(a)
              field_5_806 = str(field_5_806[0])

            if y == 48:

              l = []
              for x in range(48, 50):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_6_806.append(a)
              field_6_806 = str(field_6_806[0])

            if y == 49:
              l = []
              for x in range(50, 56):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                MAC_Sender_806.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Sender_806])
              MAC_Sender_806 = resultat
              MAC_Sender_trad_806 = formater_adresse_mac(MAC_Sender_806)
              if MAC_Sender_trad_806 in MAC.keys():
                transfert = MAC[MAC_Sender_trad_806]
                MAC_Sender_trad_806 += " "
                MAC_Sender_trad_806 += transfert
                MAC_Sender_806 = MAC_Sender_trad_806

            if y == 57:

              l = []
              for x in range(56, 60):
                l.append(listecomplete[i][x])
              a = l
              Sender_IP_806.append(a)
              chaine = ""
              compteurip = 0
              for bb in Sender_IP_806[0]:
                compteurip += 1
                if compteurip == 4:
                  chaine += str(bb)
                else:
                  chaine += str(bb)
                  chaine += "."
              # gestion adresse IP et transfert
              Sender_IP_806 = chaine
              Sender_IP_trad_806 = Sender_IP_806
              if Sender_IP_trad_806 in IP.keys():
                transfert = IP[Sender_IP_trad_806]
                Sender_IP_806 += " "
                Sender_IP_806 += transfert

            if y == 61:
              l = []
              for x in range(60, 66):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                MAC_Target_806.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Target_806])
              MAC_Target_806 = resultat
              MAC_Target_trad_806 = formater_adresse_mac(MAC_Target_806)
              if MAC_Target_trad_806 in MAC.keys():
                transfert = MAC[MAC_Target_trad_806]
                MAC_Target_trad_806 += " "
                MAC_Target_trad_806 += transfert
                MAC_Target_806 = MAC_Target_trad_806

            if y == 67:

              l = []
              for x in range(66, 70):
                l.append(listecomplete[i][x])
              a = l
              Target_IP_806.append(a)
              chaine = ""
              compteurip = 0
              for bb in Target_IP_806[0]:
                compteurip += 1
                if compteurip == 4:
                  chaine += str(bb)
                else:
                  chaine += str(bb)
                  chaine += "."
              Target_IP_806 = chaine
              Target_IP_trad_806 = Target_IP_806
              if Target_IP_trad_806 in IP.keys():
                transfert = IP[Target_IP_trad_806]
                Target_IP_806 += " "
                Target_IP_806 += transfert

          # toutes les valeurs de la trame 800 sont mise Nul

          Frame_Date = "Nul"
          MT = "Nul"
          bench_3 = "Nul"
          bench_5 = "Nul"
          Frame_Size = "Nul"
          MAC_Dest = "Nul"
          MAC_Source = "Nul"
          field_1 = "Nul"
          field_2 = "Nul"
          field_3 = "Nul"
          field_4 = "Nul"
          field_5 = "Nul"
          field_6 = "Nul"
          field_7 = "Nul"
          Source_IP = "Nul"
          Dest_IP = "Nul"
          field_9 = "Nul"
          field_10 = "Nul"
          field_11 = "Nul"
          field_14 = "Nul"
          field_16 = "Nul"
          field_17 = "Nul"
          field_18 = "Nul"
          field_20 = ["Nul"]
          field_21 = ["Nul"]
          field_23 = "Nul"
          field_25 = "Nul"
          field_26 = "Nul"
          field_28 = "Nul"
          field_29 = "Nul"
          field_30 = "Nul"
          field_32 = "Nul"
          field_33_34_35 = "Nul"

          # On crée alors une liste 800 et une liste 806
          nouvliste800 = [
            Frame_Date, MT, bench_3, bench_5, Frame_Size, MAC_Dest, MAC_Source,
            field_1, field_2, field_3, field_4, field_5, field_6, field_7,
            Source_IP, Dest_IP, field_9, field_10, field_11, field_14, field_16,
            field_17, field_18, field_20[0], field_21[0], field_23, field_25,
            field_26, field_28, field_29, field_30, field_32, field_33_34_35
          ]
          nouvliste806 = [
            Frame_Date_806, bench_3_806, bench_5_806, Frame_Size_806, MAC_Dest_806, MAC_Source_806,
            field_1_806, field_2_806, field_3_806, field_4_806, field_5_806, field_6_806, MAC_Sender_806,
            Sender_IP_806, MAC_Target_806, Target_IP_806
          ]

        # gestion trame 800
        else:
          # variable de la trame 800
          bench_1 = []
          Frame_Date = []
          bench_3 = []
          bench_4vide = []
          bench_4 = []
          bench_5 = []
          bench_6 = []
          Frame_Size = []
          MAC_Dest = []
          MAC_Source = []
          field_1 = []
          field_2 = []
          field_3 = []
          field_4 = []
          field_5 = []
          field_6 = []
          field_7 = []
          field_8 = []
          Source_IP = []
          Dest_IP = []
          field_9 = []
          field_10 = []
          field_11 = []
          field_12 = []
          field_13vide = []
          field_13 = []
          field_14 = []
          field_15 = []
          field_16 = []
          field_17 = []
          field_18 = []
          field_19vide = []
          field_19 = []
          field_20 = []
          field_21 = []
          field_22vide = []
          field_22 = []
          field_23 = []
          field_24 = []
          field_25 = []
          field_26 = []
          field_27vide = []
          field_27 = []
          field_28 = []
          field_29vide = []
          field_29 = []
          field_30 = []
          field_31 = []
          field_32 = []
          field_33 = []
          field_33_34_35 = []
          field_34 = []
          field_35 = []
          field_36 = []
          MT = [] # aussi appellé PMID

          for y in range(len(listecomplete[i])):

            if y == 0:

              l = []
              for x in range(0, 8):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              bench_1.append(a)
              bench_1 = str(bench_1[0])

            if y == 8:

              l = []
              for x in range(8, 16):
                l.append(listecomplete[i][x])
              a = l
              Frame_Date = a
              # gestion avec ieee754 
              nombre_secondes = ieee754_double(Frame_Date)
              date = secondes_vers_date(nombre_secondes)
              Frame_Date = date

            if y == 16:

              l = []
              for x in range(16, 20):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              bench_3.append(a)
              bench_3 = str(bench_3[0])

            if y == 20:
              for x in range(20, 24):
                bench_4vide.append(listecomplete[i][x])
              a = listeoctets_vers_binaire(bench_4vide)
              for ab in range(len(a)):
                if 0 <= ab <= 11:
                  bench_4.append(a[ab])
                elif 12 <= ab <= 15:
                  bench_5.append(a[ab])
                else:
                  bench_6.append(a[ab])
              bench_4_bis = []
              bench_4_bis.append(binaire_vers_decimal(bench_4))
              bench_4 = bench_4_bis
              bench_5_bis = []
              bench_5_bis.append(binaire_vers_decimal(bench_5))
              bench_5 = bench_5_bis[0]
              bench_5_trad = decimal_vers_hexadecimal(bench_5)
              bench_5 = str(bench_5)
              bench_5_trad = bench_5
              if bench_5_trad in FT_0.keys():
                transfert = FT_0[bench_5_trad]
                bench_5 += " " + transfert
              bench_6_bis = []
              bench_6_bis.append(binaire_vers_decimal(bench_6))
              bench_6 = bench_6_bis

            if y == 24:
              l = []
              for x in range(24, 28):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              Frame_Size.append(a)
              Frame_Size = str(Frame_Size[0])

            if y == 28:
              l = []
              for x in range(28, 34):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                MAC_Dest.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Dest])
              MAC_Dest = resultat
              MAC_Dest_trad = formater_adresse_mac(MAC_Dest)
              if MAC_Dest_trad in MAC.keys():
                transfert = MAC[MAC_Dest_trad]
                MAC_Dest_trad += " "
                MAC_Dest_trad += transfert
                MAC_Dest = MAC_Dest_trad

            if y == 34:
              l = []
              for x in range(34, 40):
                l.append(listecomplete[i][x])
              a = l
              for z in a:
                MAC_Source.append(decimal_vers_hexadecimal(z))
              resultat = ":".join([chaine[2:] for chaine in MAC_Source])
              MAC_Source = resultat
              MAC_Source_trad = formater_adresse_mac(MAC_Source)
              if MAC_Source_trad in MAC.keys():
                transfert = MAC[MAC_Source_trad]
                MAC_Source_trad += " "
                MAC_Source_trad += transfert
                MAC_Source = MAC_Source_trad

            if y == 40:

              l = []
              for x in range(40, 42):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              a = decimal_vers_hexadecimal(a)
              field_1.append(a)
              field_1 = str(field_1[0])

            if y == 42:

              l = []
              for x in range(42, 44):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_2.append(a)
              field_2 = str(field_2[0])

            if y == 44:

              l = []
              for x in range(44, 46):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_3.append(a)
              field_3 = str(field_3[0])

            if y == 46:

              l = []
              for x in range(46, 48):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_4.append(a)
              field_4 = str(field_4[0])

            if y == 48:

              l = []
              for x in range(48, 50):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_5.append(a)
              field_5 = str(field_5[0])

            if y == 50:

              l = []
              l.append(listecomplete[i][50])
              a = listebinaire_vers_decimal(l)
              field_6.append(a)
              field_6 = str(field_6[0])

            if y == 51:

              l = []
              l.append(listecomplete[i][51])
              a = listebinaire_vers_decimal(l)
              field_7.append(a)
              field_7 = str(field_7[0])

            if y == 52:

              l = []
              for x in range(52, 54):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_8.append(a)
              field_8 = str(field_8[0])

            if y == 54:

              l = []
              for x in range(54, 58):
                l.append(listecomplete[i][x])
              a = l
              Source_IP.append(a)
              chaine = ""
              compteurip = 0
              for bb in Source_IP[0]:
                compteurip += 1
                if compteurip == 4:
                  chaine += str(bb)
                else:
                  chaine += str(bb)
                  chaine += "."
              Source_IP = chaine
              Source_IP_trad = Source_IP
              if Source_IP_trad in IP.keys():
                transfert = IP[Source_IP_trad]
                Source_IP += " "
                Source_IP += transfert

            if y == 58:

              l = []
              for x in range(58, 62):
                l.append(listecomplete[i][x])
              a = l
              Dest_IP.append(a)
              chaine = ""
              compteurip = 0
              for bb in Dest_IP[0]:
                compteurip += 1
                if compteurip == 4:
                  chaine += str(bb)
                else:
                  chaine += str(bb)
                  chaine += "."
              Dest_IP = chaine
              Dest_IP_trad = Dest_IP
              if Dest_IP_trad in IP.keys():
                transfert = IP[Dest_IP_trad]
                Dest_IP += " "
                Dest_IP += transfert

            if y == 62:

              l = []
              for x in range(62, 64):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_9.append(a)
              field_9 = str(field_9[0])

            if y == 64:

              l = []
              for x in range(64, 66):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_10.append(a)
              field_10 = str(field_10[0])

            if y == 66:

              l = []
              for x in range(66, 68):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_11.append(a)
              field_11 = str(field_11[0])

            if y == 68 or y == 69:

              l = []
              for x in range(68, 70):
                l.append(listecomplete[i][y])
              a = listebinaire_vers_decimal(l)
              field_12.append(a)

            if y == 70:
              for x in range(70, 72):
                field_13vide.append(listecomplete[i][x])
              a = listeoctets_vers_binaire(field_13vide)
              for ab in range(len(a)):
                if ab == 0 or ab == 1:
                  field_13.append(a[ab])
                elif ab == 2:
                  field_14.append(a[ab])
                elif ab == 3:
                  field_15.append(a[ab])
                elif 4 <= ab <= 6:
                  field_16.append(a[ab])
                elif 7 <= ab <= 9:
                  field_17.append(a[ab])
                else:
                  field_18.append(a[ab])
              field_13_bis = []
              field_13_bis.append(binaire_vers_decimal(field_13))
              field_13 = field_13_bis
              field_13 = str(field_13[0])
              field_14_bis = []
              field_14_bis.append(binaire_vers_decimal(field_14))
              field_14 = field_14_bis
              field_14 = field_14[0]
              MT.append(field_14)
              field_14_trad = decimal_vers_hexadecimal(field_14)

              if field_14_trad in FT_7.keys():
                transfert = FT_7[field_14_trad]
                field_14 = str(field_14)
                field_14 += " " + transfert
              field_15_bis = []
              field_15_bis.append(binaire_vers_decimal(field_15))
              field_15 = field_15_bis
              field_15 = str(field_15[0])
              field_16_bis = []
              field_16_bis.append(binaire_vers_decimal(field_16))
              field_16 = field_16_bis
              field_16 = str(field_16[0])
              field_17_bis = []
              field_17_bis.append(binaire_vers_decimal(field_17))
              field_17 = field_17_bis
              field_17 = field_17[0]
              field_17_trad = decimal_vers_hexadecimal(field_17)
              field_17_trad = field_17_trad[:2] + field_17_trad[3:]

              if field_17_trad in FT_5.keys():
                transfert = FT_5[field_17_trad]
                field_17 = str(field_17)
                field_17 += " " + transfert

              field_18_bis = []
              field_18_bis.append(binaire_vers_decimal(field_18))
              field_18 = field_18_bis
              field_18 = field_18[0]
              MT.append(field_18)
              field_18_trad = decimal_vers_hexadecimal(field_18)

              if field_18_trad in FT_2.keys():
                transfert = FT_2[field_18_trad]
                field_18 = str(field_18)
                field_18 += " " + transfert

            if y == 72 or y == 73:

              for x in range(72, 74):
                field_19vide.append(listecomplete[i][x])
              a = listeoctets_vers_binaire(field_19vide)
              for ab in range(len(a)):
                if 0 <= ab <= 1:
                  field_19.append(a[ab])
                elif 2 <= ab <= 15:
                  field_20.append(a[ab])
              field_19_bis = []
              field_19_bis.append(binaire_vers_decimal(field_19))
              field_19 = field_19_bis
              field_20_bis = []
              field_20_bis.append(binaire_vers_decimal(field_20))
              field_20 = field_20_bis

            if y == 74 or y == 75:

              l = []
              for x in range(74, 76):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_21.append(a)

            if y == 76:

              field_22vide.append(listecomplete[i][76])
              a = listeoctets_vers_binaire(field_22vide)
              for ab in range(len(a)):
                if ab == 0 or ab == 3:
                  field_22.append(a[ab])
                elif ab == 4:
                  field_23.append(a[ab])
                elif ab == 5:
                  field_24.append(a[ab])
                elif ab == 6:
                  field_25.append(a[ab])
                else:
                  field_26.append(a[ab])
              field_22_bis = []
              field_22_bis.append(binaire_vers_decimal(field_22))
              field_22 = field_22_bis
              field_22 = str(field_22[0])
              field_23_bis = []
              field_23_bis.append(binaire_vers_decimal(field_23))
              field_23 = field_23_bis
              field_23 = str(field_23[0])
              field_24_bis = []
              field_24_bis.append(binaire_vers_decimal(field_24))
              field_24 = field_24_bis
              field_24 = str(field_24[0])
              field_25_bis = []
              field_25_bis.append(binaire_vers_decimal(field_25))
              field_25 = field_25_bis
              field_25 = str(field_25[0])
              field_26_bis = []
              field_26_bis.append(binaire_vers_decimal(field_26))
              field_26 = field_26_bis
              field_26 = str(field_26[0])

            if y == 77:

              field_27vide.append(listecomplete[i][77])
              a = listeoctets_vers_binaire(field_27vide)
              for ab in range(len(a)):
                if 0 <= ab <= 1:
                  field_27.append(a[ab])
                elif 2 <= ab <= 7:
                  field_28.append(a[ab])
              field_27_bis = []
              field_27_bis.append(binaire_vers_decimal(field_27))
              field_27 = field_27_bis
              field_27 = str(field_27[0])
              field_28_bis = []
              field_28_bis.append(binaire_vers_decimal(field_28))
              field_28 = field_28_bis
              field_28 = field_28[0]
              MT.append(field_28)
              field_28_trad = decimal_vers_hexadecimal(field_28)

              if field_28_trad in FT_3.keys():
                transfert = FT_3[field_28_trad]
                field_28 = str(field_28)
                field_28 += " " + transfert

            if y == 78:

              for x in range(78, 80):
                field_29vide.append(listecomplete[i][x])
              a = listeoctets_vers_binaire(field_29vide)
              for ab in range(len(a)):
                if 0 <= ab <= 5:
                  field_29.append(a[ab])
                elif 6 <= ab <= 15:
                  field_30.append(a[ab])
              field_29_bis = []
              field_29_bis.append(binaire_vers_decimal(field_29))
              field_29 = field_29_bis
              field_29 = field_29[0]
              MT.append(field_29)
              field_29_trad = decimal_vers_hexadecimal(field_29)

              if field_29_trad in FT_4.keys():
                transfert = FT_4[field_29_trad]
                field_29 = str(field_29)
                field_29 += " " + transfert

              field_30_bis = []
              field_30_bis.append(binaire_vers_decimal(field_30))
              field_30 = field_30_bis[0]
              MT.append(field_30)
              field_30 = str(field_30)

            if y == 80:

              l = []
              l.append(listecomplete[i][80])
              a = listebinaire_vers_decimal(l)
              field_31.append(a)
              field_31 = str(field_31[0])

            if y == 81:

              l = []
              l.append(listecomplete[i][81])
              a = listebinaire_vers_decimal(l)
              field_32.append(a)
              field_32 = field_32[0]
              field_32_trad = decimal_vers_hexadecimal(field_32)

              if field_32_trad in FT_1.keys():
                transfert = FT_1[field_32_trad]
                field_32 = str(field_32)
                field_32 += " " + transfert

            if y == 82:

              l = []
              for x in range(82, 86):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_33_34_35.append(a)
              field_33_34_35 = str(field_33_34_35[0])

              l = []
              for x in range(86, 88):
                l.append(listecomplete[i][x])
              bbb = l[0]
              a = listebinaire_vers_decimal(l)
              field_35.append(a)
              field_35 = str(field_35[0])

              field_33_34_35 = int(field_33_34_35) + bbb
              field_33_34_35 = str(field_33_34_35)

            if y == 88:

              l = []
              for x in range(88, 90):
                l.append(listecomplete[i][x])
              a = listebinaire_vers_decimal(l)
              field_36.append(a)
              field_36 = str(field_36[0])

          Frame_Date_806 = "Nul"
          bench_3_806 = "Nul"
          bench_5_806 = "Nul"
          Frame_Size_806 = "Nul"
          MAC_Dest_806 = "Nul"
          MAC_Source_806 = "Nul"
          field_1_806 = "Nul"
          field_2_806 = "Nul"
          field_3_806 = "Nul"
          field_4_806 = "Nul"
          field_5_806 = "Nul"
          field_6_806 = "Nul"
          MAC_Sender_806 = "Nul"
          Sender_IP_806 = "Nul"
          MAC_Target_806 = "Nul"
          Target_IP_806 = "Nul"


          MT = convert_decimals_to_hexadecimal(MT)
          if MT in FT_6.keys():
            transfert = FT_6[MT]
            MT = str(MT)
            MT += " " + transfert

          nouvliste806 = [
            Frame_Date_806, bench_3_806, bench_5_806, Frame_Size_806, MAC_Dest_806, MAC_Source_806,
            field_1_806, field_2_806, field_3_806, field_4_806, field_5_806, field_6_806, MAC_Sender_806,
            Sender_IP_806, MAC_Target_806, Target_IP_806
          ]
          nouvliste800 = [
            Frame_Date, MT, bench_3, bench_5, Frame_Size, MAC_Dest, MAC_Source,
            field_1, field_2, field_3, field_4, field_5, field_6, field_7,
            Source_IP, Dest_IP, field_9, field_10, field_11, field_14, field_16,
            field_17, field_18, field_20[0], field_21[0], field_23, field_25,
            field_26, field_28, field_29, field_30, field_32, field_33_34_35
          ]

        # insertion en sql de nos trames traduites

        sql2 = "INSERT INTO fichiers VALUES (%s,%s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Définir les valeurs à insérer
        values2 = (nomfichier,valeur_date_heure, Frame_Date, MT, bench_3, bench_5, Frame_Size, MAC_Dest, MAC_Source,
          field_1, field_2, field_3, field_4, field_5, field_6, field_7,
          Source_IP, Dest_IP, field_9, field_10, field_11, field_14, field_16,
          field_17, field_18, field_20[0], field_21[0], field_23, field_25,
          field_26, field_28, field_29, field_30, field_32, field_33_34_35, Frame_Date_806, bench_3_806, bench_5_806, Frame_Size_806, MAC_Dest_806, MAC_Source_806,
            field_1_806, field_2_806, field_3_806, field_4_806, field_5_806, field_6_806, MAC_Sender_806,
            Sender_IP_806, MAC_Target_806, Target_IP_806)

        # Exécuter la requête avec les valeurs

        mycursor.execute(sql2, values2)

        # Valider les changements dans la base de données
        mydb.commit()

        listecompletetraduite.append(nouvliste800 + nouvliste806)


  # execution de la focntion principale
  sniffeur(nomfic)

  # un print après l'éxecution complete pour montrer que c'est fini
  print("le fichier a bien été transféré")



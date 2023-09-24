<?php

echo '<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Projet Sniffer Thales</title>
  <link href="style.css" rel="stylesheet" type="text/css" />
</head>';

echo '<body align="center">
  <div class="header">
    <h1>Projet Sniffer Thales</h1>
  </div>

  <p class="flottegauche">
    <a href="https://www.thalesaleniaspace.com/fr/news/thales-alenia-space-lance-son-nouveau-site-internet"
      target="_parent">
      <img class="logo-thales" src="Thales_Alenia_Space_Logo.png" alt="logo-thales"></a>

  <p class="flottedroite">
    <a href="https://www.facebook.com/RTSophia/" target="_parent">
      <img class="logo-rt" src="Logo_IUT_RT.jpg" alt="logo-rt"></a>
  </p>
  <br><br><br><br><a href="index.php"><button>Retour &agrave; la page principale</button></a><br><br><br>';

  if (isset($_GET['fichierasupprimer'])) {
    $fichierasupprimer = $_GET['fichierasupprimer'];
  }
  if (isset($_GET['filtredate'])) {
    $filtredate = $_GET['filtredate'];
  }

      // Connexion à la base de données
      $host = "localhost";
      $user = "root";
      $password = "";
      $dbname = "FT";

      $conn = new mysqli($host, $user, $password, $dbname);

      // Vérifier la connexion
      if ($conn->connect_error) {
        die("La connexion a échoué: " . $conn->connect_error);
      }

      // Construire la requête SQL

      $sql = "DELETE FROM fichiers WHERE nom='$fichierasupprimer' and datetimefichier = '$filtredate'";
      $sql2 = "DELETE FROM transfert WHERE nomfichier='$fichierasupprimer' and DateTime='$filtredate'";

      //RENAME COLUMN ancien_nom_colonne2 TO nouveau_nom_colonne2

      // Exécuter la requête SQL
      if ($conn->query($sql) === TRUE) {
        echo "<br><br><br><br><center>Le fichier de transfert sélectionné a bien été supprimé.";

        // Temps en secondes avant la redirection
      $temps = 3;
      // URL de la page de destination
      $url = "http://localhost/";

      // Attente de $temps secondes avant la redirection
      header("Refresh:$temps; url=$url");

      // Affichage d'un message de redirection
      echo "<br><br>Vous allez être redirigé vers $url dans $temps secondes...</center>";


      } else {
        echo "Erreur: " . $sql . "<br>" . $conn->error;
      }

    if ($conn->query($sql2) === TRUE) {

    } else {
      echo "Erreur: " . $sql2 . "<br>" . $conn->error;
    }

  // Fermer la connexion
  $conn->close();

  echo '<div>
    <p>Cr&eacute;e par Tom Mathis, Michael Chauvet et Anthony Belle, étudiants en BUT R&T !</p>
   
    <a href="aide.html" target="_blanck">
      <button>Aide</button></a>
  </div></body></html>';



?>
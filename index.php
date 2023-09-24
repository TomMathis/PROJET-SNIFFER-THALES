<?php
session_start();
error_reporting(E_ALL);
ini_set("display_errors", 1);
 
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
  </p>';

  echo '<br><br><br><br><h2>VOIR LES TESTS TRANSFERES ET FILTRE PAR DATE D\'EXECUTION</h2>';

  echo '<form action="action.php" method="post">';

  $servername = "localhost";
  $username = "root";
  $password = "";
  $dbname = "FT";
  
  $bdd = new PDO("mysql:host=$servername;dbname=$dbname;charset=utf8", $username, $password, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
  $datas = $bdd->query("SELECT DISTINCT nom FROM fichiers");
  echo '<big>S&eacute;lectionnez le fichier &agrave; afficher et cliquez sur le bouton pour lancer la requ&ecirc;te : <select id="select-fichier" name="fichier"></big>';
  echo '<option value="" selected><big>Sélectionner le test</big></option>';
  while (False != ($data = $datas->fetch())) {
  
      $fichier=$data["nom"];
      
      echo '<option value="'.$fichier.'">' .$fichier .' </option>';
    
  }
  
  echo '</select>';
  
  echo '<script>document.getElementById("select-fichier").onchange = function() {
    var valeurSelect = this.value;
    document.getElementById("valeur-select").innerHTML = "<br><br>Vous avez sélectionné le TEST : " + valeurSelect;
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        // La requête a été effectuée avec succès
        var response = this.responseText;
        console.log(response);
      }
    };
    xhttp.open("POST", "", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("valeurSelect=" + valeurSelect);
  }
  
  
  }
  
  </script>';
  echo '<div id="valeur-select"></div>';


//Filtre par date et heure
//Modification des colonnes de la BDD
$conn = new mysqli($servername, $username, $password, $dbname);

// Verification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$SQLnompremierecolonne = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'fichiers' AND TABLE_SCHEMA = 'FT' AND ORDINAL_POSITION=2";
$result3 = $conn->query($SQLnompremierecolonne);
while($row = $result3->fetch_assoc()) {
  $nompremierecolonne=$row["COLUMN_NAME"];

}



echo '<br><br>Date d\'exécution du test : ';
echo '<form method="post" action="action-filtre.php">';
echo '<select name="filtredate">';
$SQLdateheure = "SELECT DISTINCT $nompremierecolonne FROM fichiers";
$result4 = $conn->query($SQLdateheure);
echo '<option value="TOUTES">TOUTES LES DATES ET HEURES</option>';
while($row = $result4->fetch_assoc()) {
  echo '<option value='.str_replace(" ", "-",$row[$nompremierecolonne]).'>' .$row[$nompremierecolonne] .' </option>';
}
echo '</select><br><br>';


//supression des trames
echo ' <button type="submit" name="supprimer" value="supprimer"><big>Supprimer la date d\'exécution du test sélectionné</big></button>      ';
echo ' <button type="submit" name="voirtrame" value="voirtrame"><big>Voir les trames</big></button>';

echo '</form>';






echo '<br><br><h2>RENOMMER LES COLONNES DE LA BASE DE DONNEES</h2>';

//Modification des colonnes de la BDD
$conn = new mysqli($servername, $username, $password, $dbname);

// Verification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);
echo '<br><br>';
$num=1;
echo '<form method="post" action="update_sql_colonnes.php">';

echo '<big>Sélectionnez la colonne de la base de données à modifier : <select name="colonne"></big>';
while($row = $result2->fetch_assoc()) {
  if ($row["Field"]<>'nom' and $row["Field"]<>'datetimefichier'){

		echo '<option value='.$row["Field"].'>' .$row["Field"] .' </option>';
    $num++;

  }
}

echo '</select>';
echo ' <input type="text" name="nom_colonne"> ';

echo '<button type="submit" name="submit"><big>Renommer les colonnes</big></button>';
echo '</form>';



echo '<div class="footer" ><footer>
    <p>Cr&eacute;e par Tom Mathis et Michael Chauvet et Anthony Belle, étudiants au BUT R&T de Sophia</p>
    </footer>
    <a href="aide.html" target="_blank"><img src="button_aide.png" alt="Bouton Aide"></a>
  </div></body></html>';
 
?>
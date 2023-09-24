<?php
//session_start();
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
  
if (isset($_POST['supprimer'])) {
 

    $fichierasupprimer = $_POST["fichier"];
    $datefiltrerecuperee = $_POST["filtredate"];
    $formatdate = "Y-m-d-H:i:s";
    $filtredate = DateTime::createFromFormat($formatdate, $datefiltrerecuperee)->format("Y-m-d H:i:s");

    echo '<script>
    function showConfirmation() {
      if (confirm("Voulez-vous vraiment supprimer ce fichier de transfert ?")) {
        window.location.href = "supprimer.php?fichierasupprimer='.$fichierasupprimer.'&filtredate='.$filtredate.'";
      } else {
        window.location.href = "http://localhost/index.php";
      }
    }
    </script>';
    
    echo '<script>
window.onload = function() {
  showConfirmation();
};
</script>';


 
  } elseif (isset($_POST['voirtrame'])) {
 
    echo '<br><br><br><br><a href="index.php"><button>Retour &agrave; la page principale</button></a><br><br><br>';

    // on affiche les trames

    if( !empty($_POST['fichier']) )
        {
 
                        echo "<center>Vous avez choisi d'afficher : <b>".$_POST['fichier']."</b><br><br>";
 $fichierselectionne=$_POST['fichier'];
        }


        $datefiltrerecuperee = $_POST["filtredate"];
        if ($datefiltrerecuperee=='TOUTES'){
          $filtredate = 'TOUTES';
        } else {
          $formatdate = "Y-m-d-H:i:s";
          $filtredate = DateTime::createFromFormat($formatdate, $datefiltrerecuperee)->format("Y-m-d H:i:s");
        }
        

      

if ($filtredate=='TOUTES') {
echo '<form method="post" action="exportexceltoutestrames.php">';
echo '<input type="hidden" id="datatodisplay" name="datatodisplay">';
echo '<input name="fichier" value="'.$fichierselectionne.'" type="hidden">';
echo '<div class="flottegauche"><input type="submit" value="Exporter le tableau en Excel"></div><br>    ';
echo '</form></center>';


$servername = "localhost";
$username = "root";
$password = "";
$dbname = "FT";


$conn = new mysqli($servername, $username, $password, $dbname);

// Verification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


// Nombre de lignes à afficher par page
$rows_per_page = 100;

// Numéro de la page actuelle
if (isset($_GET['page'])) {
$current_page = $_GET['page'];
} else {
$current_page = 1;
}

// Calcul de l'offset
$offset = ($current_page - 1) * $rows_per_page;

// Execution de la requête SELECT pour compter le nombre total de résultats
$count_sql = "SELECT COUNT(*) as count FROM fichiers where nom= '$fichierselectionne'";
$count_result = $conn->query($count_sql);
$count_row = $count_result->fetch_assoc();
$total_rows = $count_row['count'];




// Affichage des liens de pagination

$total_pages = ceil($total_rows / $rows_per_page);
$debut=500;
$fin=1000;


echo '<div style="text-align: center;">Page 1 ';
for ($i = 2; $i <= $total_pages; $i++) {

  echo '<a href="http://localhost/action_suite.php?page='.$i.'&debut='.$debut.'&fin='.$fin.'&fichier='.$fichierselectionne.'">'.$i.'</a> ';
  $debut=$debut+$rows_per_page;
  $fin=$fin+$rows_per_page;

}
echo '</div>';

// Execution de la requete SELECT
$sql = "SELECT * FROM fichiers where nom= '$fichierselectionne' LIMIT $offset, $rows_per_page";
$result = $conn->query($sql);

$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);
$Nombredetrame=0;



// Affichage des résultats dans un tableau HTML
if ($result->num_rows > 0) {
  echo '<div style="overflow: auto; height: 500px;"><table border=1 align=center>';
  echo '<thead><tr>';
    while($row = $result2->fetch_assoc()) {
    echo '<th>'.$row["Field"].'</th>';
    }
  echo '</tr></thead><tbody>';
    while($row = $result->fetch_assoc()) {
    echo '<tr>';
      foreach ($row as $value) {
      echo '<td>'.$value.'</td>';
      }
  echo '</tr>';
  $Nombredetrame++;
  }
  echo '</tbody></table></div>';
  }



  echo '<br><center>Nombre de trames affichées : '.$Nombredetrame.'</center><br>';



// Fermeture de la connexion de la base de donnees
$conn->close();


} else {

//Trames filtrees par date et heure

echo '<form method="post" action="exportexcelfiltredate.php">';
echo '<input type="hidden" id="datatodisplay" name="datatodisplay">';
echo '<input name="fichier" value="'.$fichierselectionne.'" type="hidden">';
echo '<input name="filtredate" value="'.$filtredate.'" type="hidden">';
echo '<div class="flottegauche"><input type="submit" value="Exporter le tableau en Excel"></div><br>    ';
echo '</form>';

echo 'FILTRE DATE D\'EXECUTION : '.$filtredate.'<br><br>';


$servername = "localhost";
$username = "root";
$password = "";
$dbname = "FT";


$conn = new mysqli($servername, $username, $password, $dbname);

// Verification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


// Nombre de lignes à afficher par page
$rows_per_page = 100;

// Numéro de la page actuelle
if (isset($_GET['page'])) {
$current_page = $_GET['page'];
} else {
$current_page = 1;
}

// Calcul de l'offset
$offset = ($current_page - 1) * $rows_per_page;

// Execution de la requête SELECT pour compter le nombre total de résultats
$count_sql = "SELECT COUNT(*) as count FROM fichiers where nom= '$fichierselectionne' and datetimefichier= '$filtredate'";
$count_result = $conn->query($count_sql);
$count_row = $count_result->fetch_assoc();
$total_rows = $count_row['count'];




// Affichage des liens de pagination

$total_pages = ceil($total_rows / $rows_per_page);
$debut=100;
$fin=1000;


echo '<div style="text-align: center;">Page 1 ';
for ($i = 2; $i <= $total_pages; $i++) {

  echo '<a href="http://localhost/action_suite_filtre.php?page='.$i.'&debut='.$debut.'&fin='.$fin.'&fichier='.$fichierselectionne.'&filtredate='.$filtredate.'">'.$i.'</a> ';
  $debut=$debut+$rows_per_page;
  $fin=$fin+$rows_per_page;

}
echo '</div>';

// Execution de la requete SELECT
$sql = "SELECT * FROM `fichiers` where `nom`= '$fichierselectionne' and datetimefichier= '$filtredate' LIMIT $offset, $rows_per_page";
$result = $conn->query($sql);

$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);
$Nombredetrame=0;



// Affichage des résultats dans un tableau HTML
if ($result->num_rows > 0) {
  echo '<div style="overflow: auto; height: 500px;"><table border=1 align=center>';
  echo '<thead><tr>';
    while($row = $result2->fetch_assoc()) {
    echo '<th>'.$row["Field"].'</th>';
    }
  echo '</tr></thead><tbody>';
    while($row = $result->fetch_assoc()) {
    echo '<tr>';
      foreach ($row as $value) {
      echo '<td>'.$value.'</td>';
      }
  echo '</tr>';
  $Nombredetrame++;
  }
  echo '</tbody></table></div>';
  }



  echo '<br><center>Nombre de trames affichées : '.$Nombredetrame.'</center><br>';



// Fermeture de la connexion de la base de donnees
$conn->close();


echo '<br><br>';


}

 
  } else {
 
  echo 'Aucune action est demandee ';

 
  }

        

echo '<div>
    <p>Cr&eacute;e par Tom Mathis et Michael Chauvet, étudiants en BUT R&T !</p>
   
    <a href="aide.html" target="_blanck">
      <button>Aide</button></a>
  </div></body></html>';



?>
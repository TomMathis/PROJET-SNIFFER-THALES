<?php
session_start();

header('Content-Type: application/force-download');
header('Content-disposition: attachment; filename=export_tableau_toutes_trames.xls');

header("Pragma: ");
header("Cache-Control: ");

?>

<?php


 $fichierselectionne=$_POST['fichier'];


 
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "FT";


$conn = new mysqli($servername, $username, $password, $dbname);

// Verification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Execution de la requ te SELECT
$sql = "SELECT * FROM `fichiers` where `nom`= '$fichierselectionne'";
$result = $conn->query($sql);

$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);
echo '<div style="overflow: auto; height: 500px;"><table border=1 align=center>';


$result = $conn->query($sql);

$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);


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

  }
  echo '</tbody></table></div>';
  }

// Fermeture de la connexion a la base de donnees
$conn->close();


?>
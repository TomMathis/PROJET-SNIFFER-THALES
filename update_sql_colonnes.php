<?php




// Récupérer les données soumises par le formulaire

session_start();
//echo $_SESSION["col1"];

$ancien_nom_colonne = $_POST["colonne"];
$nouveau_nom_colonne = $_POST["nom_colonne"];


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
$sql = "ALTER TABLE fichiers CHANGE COLUMN $ancien_nom_colonne $nouveau_nom_colonne VARCHAR(150)";

//Renommer la colonne ancien_nom_colonne en nouveau_nom_colonne

// Exécuter la requête SQL
if ($conn->query($sql) === TRUE) {
  echo "<br><br><center>La colonne a bien été modifiée.";
  // Temps en secondes avant la redirection
$temps = 5;
// URL de la page de destination
$url = "http://localhost/";

// Attente de $temps secondes avant la redirection
header("Refresh:$temps; url=$url");

// Affichage d'un message de redirection
echo "<br><br>Vous allez être redirigé vers $url dans $temps secondes...</center>";

} else {
  echo "Erreur: " . $sql . "<br>" . $conn->error;
}

// Fermer la connexion
$conn->close();
?>
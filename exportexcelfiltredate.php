<?php
session_start();

header('Content-Type: application/force-download');
header('Content-disposition: attachment; filename=export_tableau_par_date_execution.xls');
//Fix for crappy IE bug in download.
header("Pragma: ");
header("Cache-Control: ");

?>

<?php


 $fichierselectionne=$_POST['fichier'];
 $filtredate = $_POST["filtredate"];


 
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
$sql = "SELECT * FROM `fichiers` where `nom`= '$fichierselectionne' and datetimefichier= '$filtredate'";
$result = $conn->query($sql);

$nomcolonne = "SHOW COLUMNS FROM fichiers";
$result2 = $conn->query($nomcolonne);
echo '<div style="overflow: auto; height: 500px;"><table border=1 align=center>';

$num=1;


echo '<tr><thead>';
if ($result2->num_rows > 0) {
  while($row = $result2->fetch_assoc()) {
    
     echo '<th>'.$row["Field"].'</th>';
        if ($num==1) {
            $col1=$row["Field"];
           
        } else if ($num==2){ 
            $col2=$row["Field"];
            
        } else if ($num==3){ 
          $col3=$row["Field"];
     
        } else if ($num==4){ 
        $col4=$row["Field"];
       
        } else if ($num==5){ 
          $col5=$row["Field"];
         
        } else if ($num==6){ 
          $col6=$row["Field"];
          
        } else if ($num==7){ 
          $col7=$row["Field"];
          
        } else if ($num==8){ 
          $col8=$row["Field"];
          
        } else if ($num==9){ 
          $col9=$row["Field"];
          
        } else if ($num==10){ 
          $col10=$row["Field"];
          
        } else if ($num==11){ 
          $col11=$row["Field"];
          
        } else if ($num==12){ 
          $col12=$row["Field"];
          
        } else if ($num==13){ 
          $col13=$row["Field"];
          
        } else if ($num==14){ 
          $col14=$row["Field"];
          
        } else if ($num==15){ 
          $col15=$row["Field"];
        
        } else if ($num==16){ 
          $col16=$row["Field"];
       
        } else if ($num==17){ 
          $col17=$row["Field"];
         
        } else if ($num==18){ 
          $col18=$row["Field"];
          
        } else if ($num==19){ 
          $col19=$row["Field"];
         
        } else if ($num==20){ 
          $col20=$row["Field"];
          
        } else if ($num==21){ 
          $col21=$row["Field"];
          
        } else if ($num==22){ 
          $col22=$row["Field"];
          
        } else if ($num==23){ 
          $col23=$row["Field"];
          
        } else if ($num==24){ 
          $col24=$row["Field"];
          
        } else if ($num==25){ 
          $col25=$row["Field"];
          
        } else if ($num==26){ 
          $col26=$row["Field"];
         
        } else if ($num==27){ 
          $col27=$row["Field"];
          
        } else if ($num==28){ 
          $col28=$row["Field"];
        
        } else if ($num==29){ 
          $col29=$row["Field"];
         
        } else if ($num==30){ 
          $col30=$row["Field"];
      
        } else if ($num==31){ 
          $col31=$row["Field"];
         
        } else if ($num==32){ 
          $col32=$row["Field"];
         
        } else if ($num==33){ 
          $col33=$row["Field"];
       
        } else if ($num==34){ 
          $col34=$row["Field"];
        
      
    } 
     $num++;
     
  }

}
echo "</tr>";
echo "</thead><tbody>";

// Affichage des resultats dans un tableau HTML
if ($result->num_rows > 0) {

  
    while($row = $result->fetch_assoc()) {
      
        echo "<tr><td>".$row[$col1]."</td><td>".$row[$col2]."</td><td>".$row[$col3]."</td><td>".$row[$col4]."</td><td>".$row[$col5]."</td><td>".$row[$col6]."</td><td>".$row[$col7]."</td><td>".$row[$col8]."</td><td>".$row[$col9]."</td><td>".$row[$col10]."</td><td>".$row[$col11]."</td><td>".$row[$col12]."</td><td>".$row[$col13]."</td><td>".$row[$col14]."</td><td>".$row[$col15]."</td><td>".$row[$col16]."</td><td>".$row[$col17]."</td><td>".$row[$col18]."</td><td>".$row[$col19]."</td><td>".$row[$col20]."</td><td>".$row[$col21]."</td><td>".$row[$col22]."</td><td>".$row[$col23]."</td><td>".$row[$col24]."</td><td>".$row[$col25]."</td><td>".$row[$col26]."</td><td>".$row[$col27]."</td><td>".$row[$col28]."</td><td>".$row[$col29]."</td><td>".$row[$col30]."</td><td>".$row[$col31]."</td><td>".$row[$col32]."</td><td>".$row[$col33]."</td><td>".$row[$col34]."</td></tr>";
    
      }
    echo "</tbody></table></div>";

// Fermeture de la connexion a la base de donnees
$conn->close();

}

?>
<?php
require __DIR__ . '/dompdf/autoload.inc.php';

use Dompdf\Dompdf;
use Dompdf\Options;

if(isset($_GET['title'])) {
    $title = $_GET['title'];
    $title_arg = "&title=" . urlencode($title);
} else {
    $title = "---Seu nome aqui---";
    $title_arg = "";
}

$img = base64_encode(file_get_contents(__DIR__ . "/img.png"));

$date = new DateTime();
$formattedDate = $date->format('F j, Y');

$html = "<!DOCTYPE html>
<html>
<head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
    <title>SECOMPwn23 CTF Certificate</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .certificate {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #333;
        }
        p {
            color: #555;
        }
    </style>
</head>
<body>
<div class='certificate'>
    <h1>SECOMPwn23 Capture The Flag Certificate</h1>
    <p>This is to certify that</p>
    <h2>$title</h2>
    <p>has successfully completed the SECOMPwn23 Capture The Flag competition and demonstrated exceptional skills in cybersecurity and ethical hacking.</p>
    <p>Date of Completion: <strong>$formattedDate</strong></p>
    <img src='data:image/png;base64,$img'> 
</div>";


if(isset($_GET['show_export']) && !isset($_GET['pdf'])) {
    $html .= "<br/><a href=index.php?pdf$title_arg>Export to PDF</a>";
}

$html .= "</body>";
$html .= "</html>";

$html = mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8');

if (isset($_GET['pdf'])) {
    $filename = "export.pdf";

    $options = new Options();
    $options->setIsRemoteEnabled(true);

    $dompdf = new Dompdf($options);   
    $dompdf->loadHtml($html);
    $dompdf->setPaper('A5', 'portrait');

    // lets us know if something goes wrong
    global $_dompdf_show_warnings;
    $_dompdf_show_warnings = true;

    // render the HTML as PDF
    $dompdf->render();

    
    // output the generated PDF to browser
    $dompdf->stream($filename, array('Attachment' => 0));
} else {
    echo $html;
}

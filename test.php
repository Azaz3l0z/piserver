<?php
    // Las variables que tiene este php son:
    // $url: Url a descargar
    // $downloadPATH: path del PDF generado
    $url = "https://suchen.mobile.de/fahrzeuge/details.html?id=344821226&damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&isSearchRequest=true&pageNumber=1&scopeId=C&sortOption.sortBy=relevance&searchId=3d243293-1cdb-9b07-b054-96ac566f4eef"; 
    $downloadPATH = 'test.pdf';
    
    // Primero conseguimos un array con los datos
    // y la direccion del PDF en la base de datos de la API
    $data = get_data($url);
    $filename = $data['data']['pdf'];
    // Esperamos a que se genere el PDF
    sleep(20);
    // Descargamos el PDF
    get_pdf($filename, $downloadPATH);

    function get_data($url){  
        // Request URL
        $api = "azaz3l0z.ddns.net/api/importarcoches";
        $curl = curl_init();

        // Request body
        $body = array(
            "url" => $url
        );

        // Request
        curl_setopt_array($curl, array(
            CURLOPT_URL => $api,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => '',
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 0,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => 'GET',
            CURLOPT_POSTFIELDS => json_encode($body),
            CURLOPT_HTTPHEADER => array(
                'Accept: application/json',
                'Content-Type: application/json',
            ),
            CURLOPT_RETURNTRANSFER => 1
        ));

        // Response
        $resp = curl_exec($curl);
        curl_close($curl);

        return json_decode($resp, true);
    }

    function get_pdf($filename, $downloadPATH){
        $curl = curl_init();

        curl_setopt_array($curl, array(
            CURLOPT_URL => 'azaz3l0z.ddns.net/api/downloadpdf',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => '',
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 0,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => 'GET',
            CURLOPT_POSTFIELDS => 'filename='.$filename,
            CURLOPT_HTTPHEADER => array(
                'Content-Type: application/x-www-form-urlencoded'
        ),
        ));

        $response = curl_exec($curl);

        curl_close($curl);
        file_put_contents($downloadPATH, $response);
    }
?>
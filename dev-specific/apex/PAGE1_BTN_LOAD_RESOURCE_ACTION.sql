DECLARE
    l_base_url   VARCHAR2(4000);
    l_url        VARCHAR2(4000);
    l_body       CLOB;
    l_response   CLOB;
BEGIN
    SELECT ngrok_url
    INTO l_base_url
    FROM STG_RAW.NGROK_URLS
    ORDER BY created_at DESC
    FETCH FIRST 1 ROWS ONLY;

    l_url := rtrim(l_base_url, '/') || '/load';

    apex_web_service.g_request_headers(1).name  := 'Content-Type';
    apex_web_service.g_request_headers(1).value := 'application/json';

    l_body := '{"scope": "RESOURCES"}';

    l_response := apex_web_service.make_rest_request(
        p_url         => l_url,
        p_http_method => 'POST',
        p_body        => l_body
    );

    :P01_RESULT := l_response;

    -- Remplace apex_message.add_success
    apex_application.g_print_success_message :=
        'Chargement lancé (scope=RESOURCES).';

EXCEPTION
    WHEN OTHERS THEN
        apex_application.g_print_success_message :=
            'Erreur FastAPI : ' || SQLERRM;
END;

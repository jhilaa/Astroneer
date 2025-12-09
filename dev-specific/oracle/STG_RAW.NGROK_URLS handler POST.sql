DECLARE
    l_body CLOB;
BEGIN

    -- Extraire la valeur ngrok_url avec JSON_TABLE
    INSERT INTO ngrok_urls (ngrok_url)
    SELECT jt.ngrok_url
      FROM JSON_TABLE(:body, '$'
            COLUMNS (
                ngrok_url VARCHAR2(4000) PATH '$.ngrok_url'
            )
          ) jt;

    COMMIT;

    htp.p('{"status":"ok"}');
EXCEPTION
    WHEN OTHERS THEN
        htp.p('{"status":"error","message":"' || SQLERRM || '"}');
END;

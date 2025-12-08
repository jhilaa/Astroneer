DECLARE
  v_log_id NUMBER;
  v_count  NUMBER;
  v_errmsg VARCHAR2(4000);
BEGIN
  -- 1. Nouveau log_id
  SELECT STG_RAW.LOG_SEQ.NEXTVAL INTO v_log_id FROM dual;

  -- 2. Log "EN COURS" et commit immédiat
  INSERT INTO STG_RAW.LOG (log_id, table_name, log_ts)
  VALUES (v_log_id, 'STG_RAW.NAT_RES_RATE', SYSTIMESTAMP);
  COMMIT;  

  BEGIN
    -- 3. Suppression transactionnelle
    DELETE FROM STG_RAW.NAT_RES_RATE;

    -- 4. Insert en bloc depuis JSON
    INSERT INTO STG_RAW.NAT_RES_RATE (
      LOG_ID, RESOURCE_NAME, PLANETE, TAUX
    )
    SELECT v_log_id,
           jt.RESOURCE_NAME,
           jt.PLANETE,
           jt.TAUX
    FROM JSON_TABLE(:body, '$[*]'
      COLUMNS (
        resource_name   VARCHAR2(100) PATH '$.resource_name',
        planete         VARCHAR2(500)  PATH '$.planete',
        taux            VARCHAR2(500)  PATH '$.taux'
      )
    ) jt;
    v_count := SQL%ROWCOUNT;
    COMMIT;

    UPDATE STG_RAW.LOG
    SET row_count = v_count
    WHERE log_id = v_log_id;
    
    COMMIT;

    :status_code := 201;
    owa_util.mime_header('application/json', FALSE);
    owa_util.http_header_close; 
    htp.print('{"log_id": ' || v_log_id ||
              ', "status": "SUCCES"' ||
              ', "row_count": ' || v_count || '}');

  EXCEPTION
    WHEN OTHERS THEN
      v_errmsg := SQLERRM;
      ROLLBACK;

      UPDATE STG_RAW.LOG
      SET error_message = v_errmsg
      WHERE log_id = v_log_id;
      COMMIT;

      :status_code := 400;
      owa_util.mime_header('application/json', FALSE);
      owa_util.http_header_close; 
      htp.print('{"log_id": ' || v_log_id ||
                ', "status": "ECHEC"' ||
                ', "error": "' || REPLACE(v_errmsg,'"','''') || '"}');
  END;
END;
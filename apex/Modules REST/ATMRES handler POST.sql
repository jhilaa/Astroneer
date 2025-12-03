DECLARE
  v_log_id NUMBER;
  v_count  NUMBER;
  v_errmsg VARCHAR2(4000);
BEGIN
  -- 1. Nouveau log_id
  SELECT STG_RAW.LOG_SEQ.NEXTVAL INTO v_log_id FROM dual;

  -- 2. Log "EN COURS" et commit immédiat
  INSERT INTO STG_RAW.LOG (log_id, table_name, log_ts)
  VALUES (v_log_id, 'STG_RAW.ATMO_RES', SYSTIMESTAMP);
  COMMIT;  

  BEGIN
    -- 3. Suppression transactionnelle
    DELETE FROM STG_RAW.ATMO_RES;

    -- 4. Insert en bloc depuis JSON
    INSERT INTO STG_RAW.ATMO_RES (
      LOG_ID, NAME, ICON_URL
    )
    SELECT v_log_id,
           jt.NAME,
           jt.ICON_URL
    FROM JSON_TABLE(:body, '$[*]'
      COLUMNS (
        name        VARCHAR2(100) PATH '$.name',
        icon_url    VARCHAR2(500)  PATH '$.icon_url'
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
DECLARE
  v_log_id NUMBER;
  v_count  NUMBER;
  v_errmsg VARCHAR2(4000);
BEGIN
  -- 1. Nouveau log_id
  SELECT STG_RAW.LOG_SEQ.NEXTVAL INTO v_log_id FROM dual;

  -- 2. Log "EN COURS" et commit immédiat
  INSERT INTO STG_RAW.LOG (log_id, table_name, log_ts)
  VALUES (v_log_id, 'STG_RAW.PLANET', SYSTIMESTAMP);
  COMMIT;  

  BEGIN
    -- 3. Suppression transactionnelle
    DELETE FROM STG_RAW.PLANET;

    -- 4. Insert en bloc depuis JSON
    INSERT INTO STG_RAW.PLANET (
      LOG_ID, NAME, TYPE, PRIMARY_RESOURCE, SECONDARY_RESOURCE, ATMOSPHERE, DIFFICULTY, SOLAR_POWER, WIND_POWER, CORE_SYMBOL_URL, CORE_MATERIAL) 

    SELECT v_log_id,
		   jt.NAME,             
		   jt.TYPE,         		
		   jt.PRIMARY_RESOURCE,  
		   jt.SECONDARY_RESOURCE,
		   jt.ATMOSPHERE,        
		   jt.DIFFICULTY,        
		   jt.SOLAR_POWER,       
		   jt.WIND_POWER,       
		   jt.CORE_SYMBOL_URL,   
		   jt.CORE_MATERIAL        
    FROM JSON_TABLE(:body, '$[*]'
      COLUMNS (
        name             	VARCHAR2(100) PATH '$.name',
        type         		VARCHAR2(500)  PATH '$.type',
        primary_resource  	VARCHAR2(500)  PATH '$.primary_resource',
        secondary_resource  VARCHAR2(500)  PATH '$.secondary_resource',
        atmosphere         	VARCHAR2(500)  PATH '$.atmosphere',
        difficulty         	VARCHAR2(500)  PATH '$.difficulty',
        solar_power         VARCHAR2(500)  PATH '$.solar_power',
        wind_power         	VARCHAR2(500)  PATH '$.wind_power',
        core_symbol_url     VARCHAR2(500)  PATH '$.core_symbol_url',
        core_material       VARCHAR2(500)  PATH '$.core_material'
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
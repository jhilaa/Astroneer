DECLARE
  v_log_id NUMBER;
  v_count  NUMBER;
  v_errmsg VARCHAR2(4000);
BEGIN
  -- 1. Nouveau log_id
  SELECT STG_RAW.LOG_SEQ.NEXTVAL INTO v_log_id FROM dual;

  -- 2. Log "EN COURS" et commit immédiat
  INSERT INTO STG_RAW.LOG (log_id, table_name, log_ts)
  VALUES (v_log_id, 'STG_RAW.ITEM', SYSTIMESTAMP);
  COMMIT;  

  BEGIN
    -- 3. Suppression transactionnelle
    DELETE FROM STG_RAW.ITEM;

    -- 4. Insert en bloc depuis JSON
    
	INSERT INTO STG_RAW.ITEM (
      LOG_ID, 
      URL,          
      TITLE,        
      NAME,         
      ICON_SRC_URL, 
      IMG_SRC_URL,  
      TIER,         
      "GROUP",        
      "TYPE",         
      CRAFTED_AT,   
      RECIPE,       
      UNLOCK_COST       
    )
    SELECT v_log_id,
           jt.URL,          
           jt.TITLE,        
           jt.NAME,         
           jt.ICON_SRC_URL, 
           jt.IMG_SRC_URL,  
           jt.TIER,         
           jt."GROUP",        
           jt."TYPE",         
           jt.CRAFTED_AT,   
           jt.RECIPE,       
           jt.UNLOCK_COST
    FROM JSON_TABLE(:body, '$[*]'
      COLUMNS (
        url            VARCHAR2(500)   PATH '$.url',   
        title          VARCHAR2(50)    PATH '$.title',  
        name           VARCHAR2(50)    PATH '$.name',  
        icon_src_url   VARCHAR2(500)   PATH '$.icon_src_url', 
        img_src_url    VARCHAR2(500)   PATH '$.img_src_url',  
        tier           VARCHAR2(50)    PATH '$.tier',   
        "GROUP"        VARCHAR2(50)    PATH '$.group',   
        "TYPE"         VARCHAR2(50)    PATH '$.type',   
        crafted_at     VARCHAR2(50)    PATH '$.crafted_at',  
        recipe         VARCHAR2(1000)  PATH '$.recipe',  
        unlock_cost    VARCHAR2(100)   PATH '$.unlock_cost'
      )
    ) jt;
		
    v_count := SQL%ROWCOUNT;
    COMMIT;
      
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
	  
	  
	  

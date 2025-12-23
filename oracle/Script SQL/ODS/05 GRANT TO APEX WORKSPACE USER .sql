BEGIN
 -- ne fonctionne pas avec les rôles. Il faut passer par des grant sur les tables
  FOR t IN (SELECT table_name FROM all_tables WHERE owner = 'ODS') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT, UPDATE ON ODS.' || t.table_name || ' TO WKSP_';
  END LOOP;

  FOR v IN (SELECT view_name FROM all_views WHERE owner = 'ODS') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON ODS.' || v.view_name || ' TO WKSP_';
  END LOOP;

  FOR m IN (SELECT mview_name FROM all_mviews WHERE owner = 'ODS') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON ODS.' || m.mview_name || ' TO WKSP_';
  END LOOP;

  FOR s IN (SELECT sequence_name FROM all_sequences WHERE sequence_owner = 'ODS') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON ODS.' || s.sequence_name || ' TO WKSP_';
  END LOOP;
END;
-- Table des equipements
CREATE TABLE STG_RAW.ITEM (
  "URL"            VARCHAR2(500),   
  "TITLE"          VARCHAR2(50),  
  "NAME"           VARCHAR2(50),  
  "ICON_SRC_URL"   VARCHAR2(500), 
  "IMG_SRC_URL"    VARCHAR2(500),  
  "TIER"           VARCHAR2(50),   
  "GROUP"          VARCHAR2(50),   
  "TYPE"           VARCHAR2(50),   
  "CRAFTED_AT"     VARCHAR2(50),  
  "RECIPE"         VARCHAR2(1000),  
  "UNLOCK_COST"    VARCHAR2(100),  
  "LOG_ID"         NUMBER REFERENCES STG_RAW.LOG(LOG_ID)
);
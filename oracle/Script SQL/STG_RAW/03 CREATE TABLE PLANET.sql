-- Table des planètes
CREATE TABLE STG_RAW.PLANET (
  NAME              VARCHAR2(100),   -- Nom de la planète
  TYPE              VARCHAR2(100),   -- Type (ex: Lune terrestre)
  PRIMARY_RESOURCE  VARCHAR2(100),   -- Ressource principale
  SECONDARY_RESOURCE VARCHAR2(100),  -- Ressource secondaire
  ATMOSPHERE        VARCHAR2(100),   -- Atmosphère
  DIFFICULTY        VARCHAR2(50),    -- Niveau de difficulté
  SOLAR_POWER       VARCHAR2(50),    -- Puissance solaire
  WIND_POWER        VARCHAR2(50),    -- Puissance éolienne
  CORE_SYMBOL       VARCHAR2(500),   -- URL de l’icône du cœur
  CORE_MATERIAL     VARCHAR2(100),   -- Matériau du cœur
  LOG_ID            NUMBER REFERENCES STG_RAW.LOG(LOG_ID)
);
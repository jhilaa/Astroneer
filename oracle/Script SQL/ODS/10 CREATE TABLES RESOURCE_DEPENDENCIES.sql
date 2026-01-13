CREATE TABLE RESOURCE_DEPENDENCIES (
    parent_res_id    NUMBER       NOT NULL,
    child_res_id     NUMBER       NOT NULL,
	child_res_src    VARCHAR(2)   NOT NULL,   -- C1, C2 : COMPOSED, R : REFINED, A : ATMOSPHERIC
	create_ts        TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_res_dep PRIMARY KEY (parent_res_id, child_res_id, child_res_src)
);

CREATE TABLE ITEM_DEPENDENCIES (
  item_id   NUMBER PRIMARY KEY,
  tree_json CLOB,
  update_ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP NOT NULL
);


/*
CREATE TABLE RESOURCE_METADATA (
    resource_id      NUMBER PRIMARY KEY,
    color_hex        VARCHAR2(10),
    rarity_level     NUMBER,
    category         VARCHAR2(50)
);

CREATE TABLE RESOURCE_PLANET_AVAILABILITY (
    resource_id      NUMBER NOT NULL,
    planet_id        NUMBER NOT NULL,
    available_flag   CHAR(1) CHECK (available_flag IN ('Y','N')),
    CONSTRAINT pk_res_planet PRIMARY KEY (resource_id, planet_id)
);
*/

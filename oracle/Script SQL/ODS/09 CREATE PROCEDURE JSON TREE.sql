-- appel : SELECT get_resource_tree AS json_tree FROM dual;

-- dans apex : var data = &JSON_TREE.;

CREATE OR REPLACE FUNCTION get_children_json(p_parent_id NUMBER)
RETURN CLOB
IS
    l_json   CLOB := '[';
    l_first  BOOLEAN := TRUE;
BEGIN
    FOR rec IN (
        SELECT resource_id, resource_name
        FROM ods.resource_to_composed rtc
        JOIN ods.resources r ON r.resource_id IN (
            rtc.resource_atmospheric_id,
            rtc.resource_source_1_id,
            rtc.resource_source_2_id
        )
        WHERE rtc.composed_resource_id = p_parent_id
    )
    LOOP
        IF NOT l_first THEN
            l_json := l_json || ',';
        END IF;

        l_json := l_json || '{"name":"' || rec.resource_name || '"';

        -- enfants récursifs
        l_json := l_json || ',"children":' || get_children_json(rec.resource_id);

        l_json := l_json || '}';

        l_first := FALSE;
    END LOOP;

    l_json := l_json || ']';
    RETURN l_json;
END;
/


CREATE OR REPLACE FUNCTION get_resource_tree RETURN CLOB
IS
    l_json   CLOB := '[';
    l_first  BOOLEAN := TRUE;
BEGIN
    FOR root IN (
        SELECT DISTINCT r.resource_id, r.resource_name
        FROM ods.resource_to_composed rtc
        JOIN ods.resources r ON r.resource_id = rtc.composed_resource_id
    )
    LOOP
        IF NOT l_first THEN
            l_json := l_json || ',';
        END IF;

        l_json := l_json || '{"name":"' || root.resource_name || '"';
        l_json := l_json || ',"children":' || get_children_json(root.resource_id) || '}';

        l_first := FALSE;
    END LOOP;

    l_json := l_json || ']';
    RETURN l_json;
END;
/

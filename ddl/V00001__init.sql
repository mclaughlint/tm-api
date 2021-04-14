-- Initialize the database.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS api.person
(
    id             uuid    DEFAULT uuid_generate_v4() PRIMARY KEY,
    first_name     TEXT         NOT NULL,
    middle_name    TEXT,
    last_name      TEXT         NOT NULL,
    email          VARCHAR(255) NOT NULL,
    age            INTEGER      NOT NULL,
    meta_create_ts timestamptz,
    version        INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS api.person_audit
(
    -- audit trail specific attributes
    id             SERIAL PRIMARY KEY,
    stamp          timestamptz,
    db_user_id     VARCHAR(255),
    deleted        BOOLEAN      NOT NULL DEFAULT FALSE,
    -- attributes from person
    person_id      uuid         NOT NULL,
    first_name     TEXT         NOT NULL,
    middle_name    TEXT,
    last_name      TEXT         NOT NULL,
    email          VARCHAR(255) NOT NULL,
    age            INTEGER      NOT NULL,
    meta_create_ts timestamptz,
    version        INTEGER      NOT NULL DEFAULT 1
);

-- Trigger to version records on update/insert
CREATE OR REPLACE FUNCTION process_ui_audit() RETURNS TRIGGER AS $ui_audit$
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            EXECUTE 'INSERT INTO api.person_audit
                     SELECT NEXTVAL(pg_get_serial_sequence(''api.person_audit'', ''id'')),
                       now(), user, false, ($1).*'
                USING OLD;
            NEW.version = OLD.version + 1;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            NEW.version = 1;
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            EXECUTE 'INSERT INTO api.person_audit
                     SELECT NEXTVAL(pg_get_serial_sequence(''api.person_audit'', ''id'')),
                       now(), user, true, ($1).*'
                USING OLD;
            NEW.version = OLD.version + 1;
            RETURN NEW;
        END IF;
    END;
$ui_audit$ LANGUAGE plpgsql;

CREATE TRIGGER person_audit BEFORE INSERT OR UPDATE OR DELETE ON api.person
    FOR EACH ROW EXECUTE PROCEDURE process_ui_audit();
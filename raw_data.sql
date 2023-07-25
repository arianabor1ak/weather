CREATE TABLE raw_data (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    datetime_utc TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP(0),                -- internal representation of time measurement was saved
    formatted_id BIGINT,
    raw_string TEXT NOT NULL
);
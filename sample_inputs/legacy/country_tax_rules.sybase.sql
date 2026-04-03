CREATE TABLE country_tax_rules (
    country_code     VARCHAR(2)   NOT NULL,
    policy_type      VARCHAR(20)  NOT NULL,
    tax_rate         NUMERIC(9,4) NOT NULL,
    active_flag      CHAR(1)      NOT NULL,
    is_eu_member     CHAR(1)      NOT NULL,
    effective_from   DATETIME     NOT NULL,
    effective_to     DATETIME     NULL
)
go

INSERT INTO country_tax_rules VALUES ('DE', 'DEFAULT',   0.1900, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('DE', 'HEALTH',    0.2100, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('FR', 'DEFAULT',   0.1200, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('FR', 'TRAVEL',    0.1450, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('IT', 'DEFAULT',   0.0900, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('IT', 'FAMILY',    0.1100, 'Y', 'Y', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('GB', 'DEFAULT',   0.0600, 'Y', 'N', '2024-01-01', NULL)
INSERT INTO country_tax_rules VALUES ('US', 'DEFAULT',   0.0000, 'Y', 'N', '2024-01-01', NULL)

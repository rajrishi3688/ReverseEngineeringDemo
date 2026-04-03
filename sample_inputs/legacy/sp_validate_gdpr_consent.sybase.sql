CREATE PROCEDURE sp_validate_gdpr_consent
    @quote_id      INT,
    @country_code  VARCHAR(2)
AS
BEGIN
    DECLARE @is_eu_country CHAR(1)
    DECLARE @gdpr_granted  CHAR(1)

    SELECT @is_eu_country = is_eu_member
      FROM country_tax_rules
     WHERE country_code = @country_code
       AND policy_type = 'DEFAULT'

    IF @is_eu_country = 'Y'
    BEGIN
        SELECT @gdpr_granted = consent_granted
          FROM quote_context
         WHERE quote_id = @quote_id

        IF ISNULL(@gdpr_granted, 'N') <> 'Y'
        BEGIN
            INSERT INTO audit_event (
                quote_id,
                event_type,
                event_message,
                created_at
            )
            VALUES (
                @quote_id,
                'GDPR_FAILURE',
                'GDPR consent missing for EU quote processing',
                GETDATE()
            )

            RAISERROR 20002 'GDPR consent is required for EU quote processing'
            RETURN
        END
    END
END

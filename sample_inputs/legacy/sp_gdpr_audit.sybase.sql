CREATE PROCEDURE sp_gdpr_audit
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM customer_consent
        WHERE consent_type = 'GDPR'
          AND granted = 0
    )
    BEGIN
        RAISERROR 20001 'GDPR consent missing for EU customer'
        RETURN
    END
END

CREATE PROCEDURE sp_quote_eligibility
    @customer_age     INT,
    @policy_type      VARCHAR(20),
    @country_code     VARCHAR(2),
    @coverage_amount  NUMERIC(12,2)
AS
BEGIN
    IF @customer_age < 18
    BEGIN
        RAISERROR 20010 'Customer must be at least 18 years old'
        RETURN
    END

    IF @policy_type = 'TRAVEL' AND @coverage_amount > 1000000
    BEGIN
        RAISERROR 20011 'Travel policy exceeds legacy coverage limit'
        RETURN
    END

    IF @policy_type = 'HEALTH' AND @country_code NOT IN ('DE', 'FR', 'IT', 'GB')
    BEGIN
        RAISERROR 20012 'Health policy not available in selected country'
        RETURN
    END
END

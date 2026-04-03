CREATE PROCEDURE sp_calculate_quote
AS
BEGIN
    DECLARE @quote_id            INT
    DECLARE @premium             NUMERIC(12,2)
    DECLARE @age                 INT
    DECLARE @country             VARCHAR(2)
    DECLARE @policy_type         VARCHAR(20)
    DECLARE @customer_segment    VARCHAR(20)
    DECLARE @payment_frequency   VARCHAR(10)
    DECLARE @coverage_amount     NUMERIC(12,2)
    DECLARE @risk_factor         NUMERIC(12,4)
    DECLARE @discount_amount     NUMERIC(12,2)
    DECLARE @tax_amount          NUMERIC(12,2)

    SELECT
        @quote_id = quote_id,
        @premium = base_premium,
        @age = customer_age,
        @country = country_code,
        @policy_type = policy_type,
        @customer_segment = customer_segment,
        @payment_frequency = payment_frequency,
        @coverage_amount = coverage_amount
    FROM quote_context

    EXEC sp_validate_gdpr_consent @quote_id, @country
    EXEC sp_apply_risk_loading @age, @policy_type, @coverage_amount, @risk_factor OUTPUT
    EXEC sp_apply_discount_rules @customer_segment, @policy_type, @payment_frequency, @premium, @discount_amount OUTPUT
    EXEC sp_lookup_country_tax @country, @policy_type, @premium, @tax_amount OUTPUT

    SELECT @premium = (@premium * @risk_factor) - @discount_amount + @tax_amount

    IF @policy_type = 'CORPORATE'
        SELECT @premium = @premium * 1.15

    UPDATE quote_context
       SET final_premium = @premium,
           discount_amount = @discount_amount,
           tax_amount = @tax_amount,
           risk_factor = @risk_factor,
           last_updated = GETDATE()
     WHERE quote_id = @quote_id

    SELECT
        @quote_id AS quote_id,
        @premium AS final_premium,
        @discount_amount AS discount_amount,
        @tax_amount AS tax_amount,
        @risk_factor AS risk_factor
END

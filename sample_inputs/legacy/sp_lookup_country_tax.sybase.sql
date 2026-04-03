CREATE PROCEDURE sp_lookup_country_tax
    @country_code    VARCHAR(2),
    @policy_type     VARCHAR(20),
    @premium_amount  NUMERIC(12,2),
    @tax_amount      NUMERIC(12,2) OUTPUT
AS
BEGIN
    DECLARE @tax_rate NUMERIC(9,4)
    SELECT @tax_rate = tax_rate
      FROM country_tax_rules
     WHERE country_code = @country_code
       AND policy_type = @policy_type
       AND active_flag = 'Y'

    IF @tax_rate IS NULL
        SELECT @tax_rate = tax_rate
          FROM country_tax_rules
         WHERE country_code = @country_code
           AND policy_type = 'DEFAULT'
           AND active_flag = 'Y'

    IF @tax_rate IS NULL
        SELECT @tax_rate = 0

    SELECT @tax_amount = ROUND(@premium_amount * @tax_rate, 2)
END

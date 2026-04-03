CREATE PROCEDURE sp_apply_discount_rules
    @customer_segment   VARCHAR(20),
    @policy_type        VARCHAR(20),
    @payment_frequency  VARCHAR(10),
    @base_premium       NUMERIC(12,2),
    @discount_amount    NUMERIC(12,2) OUTPUT
AS
BEGIN
    DECLARE @discount_pct NUMERIC(9,4)
    SELECT @discount_pct = 0

    IF @customer_segment = 'LOYALTY_GOLD'
        SELECT @discount_pct = @discount_pct + 0.07

    IF @customer_segment = 'EMPLOYEE'
        SELECT @discount_pct = @discount_pct + 0.10

    IF @policy_type = 'FAMILY'
        SELECT @discount_pct = @discount_pct + 0.05

    IF @payment_frequency = 'ANNUAL'
        SELECT @discount_pct = @discount_pct + 0.02

    IF @discount_pct > 0.15
        SELECT @discount_pct = 0.15

    SELECT @discount_amount = ROUND(@base_premium * @discount_pct, 2)
END

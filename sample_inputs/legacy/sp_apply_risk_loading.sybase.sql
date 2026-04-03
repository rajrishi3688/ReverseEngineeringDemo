CREATE PROCEDURE sp_apply_risk_loading
    @customer_age      INT,
    @policy_type       VARCHAR(20),
    @coverage_amount   NUMERIC(12,2),
    @risk_factor       NUMERIC(12,4) OUTPUT
AS
BEGIN
    SELECT @risk_factor = 1.0000

    IF @customer_age BETWEEN 18 AND 24
        SELECT @risk_factor = @risk_factor + 0.06

    IF @customer_age >= 50
        SELECT @risk_factor = @risk_factor + 0.08

    IF @customer_age >= 65
        SELECT @risk_factor = @risk_factor + 0.05

    IF @policy_type = 'CORPORATE'
        SELECT @risk_factor = @risk_factor + 0.10

    IF @policy_type = 'TRAVEL' AND @coverage_amount > 250000
        SELECT @risk_factor = @risk_factor + 0.04

    IF @policy_type = 'HEALTH' AND @coverage_amount > 500000
        SELECT @risk_factor = @risk_factor + 0.03
END

CREATE TABLE quotes (
    quote_id UUID PRIMARY KEY,
    customer_id TEXT NOT NULL,
    policy_type TEXT NOT NULL,
    country_code TEXT NOT NULL,
    base_premium NUMERIC(12,2) NOT NULL,
    coverage_amount NUMERIC(12,2) NOT NULL,
    customer_segment TEXT,
    payment_frequency TEXT NOT NULL DEFAULT 'MONTHLY',
    risk_factor NUMERIC(10,4) NOT NULL DEFAULT 1.0000,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    final_premium NUMERIC(12,2) NOT NULL,
    consent_marketing BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

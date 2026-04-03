const { validateQuoteInput } = require('./quote.validation');
const { computeRiskFactor } = require('./rating.service');
const { computeDiscount } = require('./discount.service');
const { saveQuoteAudit } = require('./quote.audit');

const calculateQuote = (req, res) => {
  const {
    quoteId,
    customerId,
    policyType,
    age,
    basePremium,
    coverageAmount,
    customerSegment,
    paymentFrequency,
    countryCode
  } = req.body;

  validateQuoteInput({ customerId, policyType, age, coverageAmount, countryCode });

  const premium = Number(basePremium || 0);
  const riskFactor = computeRiskFactor({ age, policyType, coverageAmount });
  const discountAmount = computeDiscount({
    customerSegment,
    policyType,
    paymentFrequency,
    premium
  });

  let finalPremium = premium * riskFactor - discountAmount;

  if (policyType === 'CORPORATE') {
    finalPremium = finalPremium * 1.1;
  }

  saveQuoteAudit({
    quoteId,
    customerId,
    countryCode,
    riskFactor,
    discountAmount,
    finalPremium
  });

  res.json({
    quoteId,
    customerId,
    countryCode,
    pricing: {
      basePremium: premium,
      riskFactor,
      discountAmount,
      finalPremium
    }
  });
};

module.exports = { calculateQuote };

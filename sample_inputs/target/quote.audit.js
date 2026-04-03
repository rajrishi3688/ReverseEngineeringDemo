const saveQuoteAudit = ({ quoteId, customerId, countryCode, riskFactor, discountAmount, finalPremium }) => {
  return {
    quoteId,
    customerId,
    countryCode,
    eventType: 'QUOTE_RATED',
    payload: {
      riskFactor,
      discountAmount,
      finalPremium
    }
  };
};

module.exports = { saveQuoteAudit };

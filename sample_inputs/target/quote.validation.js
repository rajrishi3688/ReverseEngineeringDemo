const validateQuoteInput = ({ customerId, policyType, age, coverageAmount, countryCode }) => {
  if (!customerId || !policyType || !countryCode) {
    throw new Error('Required quote attributes are missing');
  }

  if (Number(age) < 18) {
    throw new Error('Customer must be at least 18 years old');
  }

  if (policyType === 'TRAVEL' && Number(coverageAmount) > 1000000) {
    throw new Error('Travel policy exceeds supported coverage limit');
  }
};

module.exports = { validateQuoteInput };

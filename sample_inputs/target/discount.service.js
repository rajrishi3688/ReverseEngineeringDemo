const computeDiscount = ({ customerSegment, policyType, paymentFrequency, premium }) => {
  let discountPct = 0;

  if (customerSegment === 'LOYALTY_GOLD') {
    discountPct += 0.05;
  }

  if (customerSegment === 'EMPLOYEE') {
    discountPct += 0.08;
  }

  if (policyType === 'FAMILY') {
    discountPct += 0.04;
  }

  if (paymentFrequency === 'ANNUAL') {
    discountPct += 0.02;
  }

  if (discountPct > 0.12) {
    discountPct = 0.12;
  }

  return Number(premium || 0) * discountPct;
};

module.exports = { computeDiscount };

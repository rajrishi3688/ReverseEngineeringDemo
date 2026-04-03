const computeRiskFactor = ({ age, policyType, coverageAmount }) => {
  let factor = 1;
  const normalizedAge = Number(age || 0);
  const normalizedCoverage = Number(coverageAmount || 0);

  if (normalizedAge >= 18 && normalizedAge <= 24) {
    factor += 0.04;
  }

  if (normalizedAge >= 50) {
    factor += 0.05;
  }

  if (normalizedAge >= 65) {
    factor += 0.03;
  }

  if (policyType === 'CORPORATE') {
    factor += 0.08;
  }

  if (policyType === 'TRAVEL' && normalizedCoverage > 250000) {
    factor += 0.03;
  }

  return factor;
};

module.exports = { computeRiskFactor };

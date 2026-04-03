export class QuoteFormComponent {
  model = {
    quoteId: '',
    customerId: '',
    policyType: '',
    countryCode: '',
    birthDate: '',
    coverageAmount: 0,
    customerSegment: '',
    paymentFrequency: 'MONTHLY',
    consentMarketing: false
  };

  submit(): void {
    if (!this.model.customerId || !this.model.policyType || !this.model.countryCode) {
      throw new Error('Missing required fields');
    }

    if (this.model.coverageAmount <= 0) {
      throw new Error('Coverage amount must be greater than zero');
    }
  }
}

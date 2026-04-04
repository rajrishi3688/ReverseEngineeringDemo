# Sample Input User Experience Guide

This document explains the sample legacy and target input systems from an end-user point of view: what the user sees on screen, what they can enter, what actions they can perform, and what outcomes they can expect.

## Legacy System: What The User Sees

The legacy sample represents a Windows desktop insurance quote application.

### Main legacy experience

When a user opens the legacy quote application, they start from a country-selection experience that opens a dedicated quote generation screen for the chosen country.

The available quote variants are:

- Germany
- Italy
- Spain
- Portugal
- Switzerland
- United Kingdom

Each variant uses the same basic quote-entry experience, but the pricing and compliance behavior changes in the background based on the selected country.

### Legacy quote screen

On the quote generation screen, the user sees a classic form-style layout with input controls for:

- Customer Id
- Customer Age
- Coverage Amount
- Policy Type
- Payment Frequency
- Customer Segment
- GDPR Consent Confirmed

The screen also shows a country-specific hint message that explains that country-level quote adjustments are active.

### What the user can do in the legacy system

The user can:

- Enter a customer identifier
- Enter the customer age
- Enter a requested coverage amount
- Choose a policy type such as `HEALTH`, `TRAVEL`, `FAMILY`, or `CORPORATE`
- Choose a payment frequency such as `MONTHLY`, `QUARTERLY`, or `ANNUAL`
- Choose a customer segment such as `STANDARD`, `LOYALTY_GOLD`, or `EMPLOYEE`
- Confirm GDPR consent where applicable
- Submit the quote using the `Generate Quote` button

### What happens when the user submits

After clicking `Generate Quote`, the system performs quote validation, pricing, tax and adjustment logic, and persistence steps in the background.

From the user’s point of view, the important functional outcomes are:

- The quote can be blocked if required values are missing
- The quote can be blocked if the customer is not eligible
- The quote can be blocked if GDPR consent is required but not granted
- The premium can change based on:
  - age
  - policy type
  - customer segment
  - payment frequency
  - country-specific pricing rules
- The result is saved as a quote record and audit trail behind the scenes

### What the user sees after submission

If the quote succeeds, the user sees a result message showing:

- Quote Id
- Final Premium
- Country Adjustment

### Functional behavior visible to the user

A business user testing the legacy system would observe these capabilities:

- Country-specific quote generation screens exist
- The form supports different insurance products
- Discounts and premiums change based on user selections
- GDPR consent matters for applicable scenarios
- The application produces a quote reference and premium result after submission

## Target System: What The User Sees

The target sample represents a web-based quote generation experience built with Angular on the frontend and a Node.js API on the backend.

### Main target experience

The target system exposes a single modern quote generation form focused on Spain.

Unlike the legacy sample, the target sample does not present multiple country-specific screens. The form is streamlined around one supported market.

### Target quote screen

On the web screen, the user sees a quote entry form with:

- Customer Id
- Age
- Policy Type
- Coverage Amount
- Customer Segment
- Payment Frequency
- GDPR consent confirmed

The country is fixed to Spain in the flow, so the user does not interact with multiple country variants.

### What the user can do in the target system

The user can:

- Enter a customer identifier
- Enter age
- choose a policy type
- Enter coverage amount
- Choose a customer segment
- Choose payment frequency
- Confirm GDPR consent
- Submit the form using `Generate Quote`

### What happens when the user submits

Once the user clicks `Generate Quote`, the web app sends the request to an API endpoint.

The user-facing functional behavior is:

- Validation happens before quote generation completes
- The flow supports Spain only
- GDPR consent is required
- The final premium is calculated using:
  - risk factor logic
  - discount logic
  - Spain tax logic
  - Spain-specific adjustment logic
- The quote is saved and an audit message is generated

### What the user sees after submission

If the quote succeeds, the result panel shows:

- Quote Id
- Final Premium
- Spain Adjustment
- Audit message

### Functional behavior visible to the user

A business user testing the target system would observe these capabilities:

- A single web-based quote screen is available
- The form is focused on Spain-only quote generation
- The user receives a quote result immediately after submission
- Premium output includes a country-specific Spain adjustment
- The experience is simpler and more standardized than the legacy variant-based screens

## Functional Comparison From A User Perspective

### Legacy user experience

- Multiple country-specific entry points
- Desktop-style forms
- Country variations are visible in the UI
- Behavior changes depending on which country screen is opened

### Target user experience

- Single web form
- Modern API-driven submission
- Country variation is not exposed as multiple screens
- The sample currently focuses only on Spain

## What A Reviewer Should Check

If this document is being used for review or GitHub check-in, the main user-visible behaviors represented by the sample inputs are:

- The legacy sample shows a multi-country quote-entry experience with several country-specific screens
- The target sample shows a simplified, web-based quote-entry experience for Spain
- Both systems allow quote data entry, quote submission, pricing calculation, and display of a quote result
- Both systems include compliance-aware behavior, especially around GDPR consent
- The target sample represents a streamlined modernization path rather than full country parity with the legacy sample

Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class GermanyCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim insuranceDuty = currentPremium * 0.032D
            Dim socialHealthSurcharge = If(request.PolicyType = "HEALTH", currentPremium * 0.014D, 0D)
            Return insuranceDuty + socialHealthSurcharge
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "Germany processing applied DE insurance duty and statutory health surcharge."
        End Function
    End Class
End Namespace

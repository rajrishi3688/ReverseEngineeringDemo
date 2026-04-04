Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class UnitedKingdomCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim ipt = currentPremium * 0.12D
            Dim travelSecurityFee = If(request.PolicyType = "TRAVEL", 6D, 0D)
            Return ipt + travelSecurityFee
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "United Kingdom processing applied insurance premium tax and travel security fee."
        End Function
    End Class
End Namespace

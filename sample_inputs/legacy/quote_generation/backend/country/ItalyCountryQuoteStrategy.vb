Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class ItalyCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim stampDuty = 22D
            Dim familyRelief = If(request.PolicyType = "FAMILY", -12D, 0D)
            Return stampDuty + familyRelief
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "Italy processing applied stamp duty and optional family relief."
        End Function
    End Class
End Namespace

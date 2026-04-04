Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class SpainCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim consortiumLevy = currentPremium * 0.018D
            Dim travelAssistReserve = If(request.PolicyType = "TRAVEL", 9.5D, 0D)
            Return consortiumLevy + travelAssistReserve
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "Spain processing applied consortium levy and travel assistance reserve."
        End Function
    End Class
End Namespace

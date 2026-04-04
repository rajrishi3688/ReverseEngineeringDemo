Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Contracts
    Public Interface ICountryQuoteStrategy
        Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal
        Function BuildCountryNote(request As QuoteRequest) As String
    End Interface
End Namespace

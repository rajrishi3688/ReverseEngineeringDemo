Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class PortugalCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim solidarityLevy = currentPremium * 0.012D
            Dim annualCollectionRelief = If(request.PaymentFrequency = "ANNUAL", -7.5D, 0D)
            Return solidarityLevy + annualCollectionRelief
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "Portugal processing applied solidarity levy and annual collection relief."
        End Function
    End Class
End Namespace

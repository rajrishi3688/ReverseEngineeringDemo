Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Country
    Public Class SwitzerlandCountryQuoteStrategy
        Implements ICountryQuoteStrategy

        Public Function ApplyCountryAdjustments(request As QuoteRequest, currentPremium As Decimal) As Decimal Implements ICountryQuoteStrategy.ApplyCountryAdjustments
            Dim cantonalReserve = currentPremium * 0.021D
            Dim corporateHandlingFee = If(request.PolicyType = "CORPORATE", 35D, 0D)
            Return cantonalReserve + corporateHandlingFee
        End Function

        Public Function BuildCountryNote(request As QuoteRequest) As String Implements ICountryQuoteStrategy.BuildCountryNote
            Return "Switzerland processing applied cantonal reserve loading and corporate handling fee."
        End Function
    End Class
End Namespace

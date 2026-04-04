Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Country
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Services
    Public Class QuoteWorkflowService
        Public Function GenerateQuote(request As QuoteRequest) As QuoteResult
            Dim strategy = ResolveStrategy(request.CountryCode)
            Dim processor As New CommonCountryQuoteProcessor(strategy)
            Return processor.ProcessQuote(request)
        End Function

        Private Function ResolveStrategy(countryCode As String) As ICountryQuoteStrategy
            Select Case countryCode
                Case "DE" : Return New GermanyCountryQuoteStrategy()
                Case "IT" : Return New ItalyCountryQuoteStrategy()
                Case "ES" : Return New SpainCountryQuoteStrategy()
                Case "PT" : Return New PortugalCountryQuoteStrategy()
                Case "CH" : Return New SwitzerlandCountryQuoteStrategy()
                Case "GB" : Return New UnitedKingdomCountryQuoteStrategy()
                Case Else : Throw New ApplicationException("Unsupported country code for legacy quote generation.")
            End Select
        End Function
    End Class
End Namespace

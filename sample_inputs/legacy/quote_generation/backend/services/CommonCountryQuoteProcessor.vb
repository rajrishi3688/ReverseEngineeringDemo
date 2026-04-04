Imports LegacyModernization.QuoteGeneration.Backend.Contracts
Imports LegacyModernization.QuoteGeneration.Backend.Data
Imports LegacyModernization.QuoteGeneration.Backend.Models

Namespace LegacyModernization.QuoteGeneration.Backend.Services
    Public Class CommonCountryQuoteProcessor
        Private ReadOnly _strategy As ICountryQuoteStrategy
        Private ReadOnly _repository As New QuoteRepository()
        Private ReadOnly _referenceRepository As New ReferenceDataRepository()
        Private ReadOnly _auditRepository As New AuditRepository()

        Public Sub New(strategy As ICountryQuoteStrategy)
            _strategy = strategy
        End Sub

        Public Function ProcessQuote(request As QuoteRequest) As QuoteResult
            Dim validationService As New QuoteValidationService(_repository, _referenceRepository)
            Dim pricingService As New QuotePricingService(_repository, _referenceRepository)
            Dim persistenceService As New QuotePersistenceService(_repository, _auditRepository)

            validationService.ValidateRequest(request)

            Dim result = pricingService.CalculateQuote(request, _strategy)
            persistenceService.PersistQuote(request, result, _strategy.BuildCountryNote(request))
            Return result
        End Function
    End Class
End Namespace

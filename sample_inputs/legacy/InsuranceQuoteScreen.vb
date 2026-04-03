Public Class InsuranceQuoteScreen
    Private Sub SaveQuote()
        If Customer.CountryCode = "DE" Then
            Premium = Premium + ApplyGermanInsuranceTax(PolicyType, Premium)
        ElseIf Customer.CountryCode = "FR" Then
            Premium = Premium + ApplyFrenchRegionalTax(PolicyType, Premium)
        ElseIf Customer.CountryCode = "IT" Then
            Premium = Premium + ApplyItalianStampDuty(PolicyType, Premium)
        End If

        If Customer.IsEuropeanUnion AndAlso Not chkGdprConsent.Checked Then
            Throw New ApplicationException("GDPR consent is required before quote save.")
        End If

        If Customer.Age > 60 Then
            Premium = Premium * 1.12D
        End If

        If cboPolicyType.SelectedValue = "FAMILY" Then
            Premium = Premium * 0.95D
        End If
    End Sub
End Class

clueReportFillable.pdf was created in LibreOffice, from clueReportFillable.odt (previously 'Clue Report.odt'), using the Form tools and 'Export as PDF'

clueReportFillable.pdf should be a pdf with fillable data fields as listed below (using pdftk <file> dump_data_fields):

C:\..\radiolog> pdftk clueReportFillable2.pdf dump_data_fields
---
FieldType: Text
FieldName: incidentNameField
FieldFlags: 0
FieldValue:
FieldJustification: Left
---
FieldType: Text
FieldName: dateField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
FieldType: Text
FieldName: operationalPeriodField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
FieldType: Text
FieldName: clueNumberField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
FieldType: Text
FieldName: dateTimeField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
FieldType: Text
FieldName: teamField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
FieldType: Text
FieldName: descriptionField
FieldFlags: 4096
FieldValue:
FieldJustification: Left
---
FieldType: Text
FieldName: locationField
FieldFlags: 4096
FieldValue:
FieldJustification: Left
---
FieldType: Button
FieldName: instructionsCollectField
FieldFlags: 0
FieldValue: Off
FieldJustification: Left
FieldStateOption: Off
FieldStateOption: Yes
---
FieldType: Button
FieldName: instructionsDisregardField
FieldFlags: 0
FieldValue: Off
FieldJustification: Left
FieldStateOption: Off
FieldStateOption: Yes
---
FieldType: Button
FieldName: instructionsMarkAndLeaveField
FieldFlags: 0
FieldValue: Off
FieldJustification: Left
FieldStateOption: Off
FieldStateOption: Yes
---
FieldType: Button
FieldName: instructionsOtherField
FieldFlags: 0
FieldValue: Off
FieldJustification: Left
FieldStateOption: Off
FieldStateOption: Yes
---
FieldType: Text
FieldName: instructionsOtherTextField
FieldFlags: 0
FieldValue:
FieldJustification: Left
---
[note, titleField was added 2-4-18 TMG to remove hardcoded 'Nevada County' title and allow configurable agency name instead]
FieldType: Text
FieldName: titleField
FieldFlags: 0
FieldValue:
FieldJustification: Center
---
[note, locationRadioGSPField was added 2-4-18 TMG; previously, any existing radio GPS text was prepended to the full location text; now it is in a separate field, on the same line as the field label]
FieldType: Text
FieldName: locationRadioGPSField
FieldFlags: 0
FieldValue:
FieldJustification: Left
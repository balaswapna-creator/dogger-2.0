"""
Dogger 2.0 - PDF Generation Utilities
Generates professional PDFs for prescriptions, certificates, reports
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
from datetime import datetime


# Brand color
BRAND_COLOR = colors.HexColor('#226C3B')


def draw_header(canvas_obj, doc):
    """Draw clinic header on each page"""
    canvas_obj.saveState()
    
    # Header rectangle
    canvas_obj.setFillColor(BRAND_COLOR)
    canvas_obj.rect(0, A4[1] - 1.5*inch, A4[0], 1.5*inch, fill=True, stroke=False)
    
    # Clinic name
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont('Helvetica-Bold', 20)
    canvas_obj.drawCentredString(A4[0]/2, A4[1] - 0.8*inch, settings.CLINIC_NAME)
    
    # Clinic address
    canvas_obj.setFont('Helvetica', 10)
    canvas_obj.drawCentredString(A4[0]/2, A4[1] - 1.05*inch, settings.CLINIC_ADDRESS)
    canvas_obj.drawCentredString(A4[0]/2, A4[1] - 1.25*inch, 
                                f"Phone: {settings.CLINIC_PHONE} | Email: {settings.CLINIC_EMAIL}")
    
    canvas_obj.restoreState()


def draw_footer(canvas_obj, doc):
    """Draw footer with signature area"""
    canvas_obj.saveState()
    
    # Footer line
    canvas_obj.setStrokeColor(BRAND_COLOR)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(0.75*inch, 1.5*inch, A4[0] - 0.75*inch, 1.5*inch)
    
    # Signature section
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.drawString(1*inch, 1.2*inch, "Veterinarian Signature:")
    canvas_obj.line(2.5*inch, 1.15*inch, 4.5*inch, 1.15*inch)
    
    canvas_obj.drawString(5*inch, 1.2*inch, "Clinic Seal:")
    canvas_obj.rect(5.8*inch, 0.8*inch, 1*inch, 0.6*inch, stroke=True, fill=False)
    
    # License info
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.drawCentredString(A4[0]/2, 0.5*inch, 
                                f"Veterinary License: {settings.CLINIC_LICENSE}")
    
    canvas_obj.restoreState()


# ============================================================================
# PRESCRIPTION PDF
# ============================================================================

def generate_prescription_pdf(medical_record):
    """
    Generate prescription PDF for a medical record
    """
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*inch,
        bottomMargin=2*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=BRAND_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=BRAND_COLOR,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("PRESCRIPTION", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Patient info table
    patient = medical_record.patient
    patient_data = [
        ['Patient Name:', patient.pet_name, 'Species:', patient.species.capitalize()],
        ['Owner Name:', patient.owner.name, 'Phone:', patient.owner.phone],
        ['Date:', medical_record.visit_date.strftime('%d-%b-%Y'), 'Age:', patient.age_string],
    ]
    
    patient_table = Table(patient_data, colWidths=[1.5*inch, 2.2*inch, 1.2*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Clinical details
    story.append(Paragraph("Chief Complaint:", heading_style))
    story.append(Paragraph(medical_record.chief_complaint or 'N/A', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Diagnosis:", heading_style))
    story.append(Paragraph(medical_record.diagnosis or 'N/A', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Vitals if available
    if medical_record.temperature or medical_record.weight or medical_record.heart_rate:
        vitals_text = []
        if medical_record.temperature:
            vitals_text.append(f"Temperature: {medical_record.temperature}°F")
        if medical_record.weight:
            vitals_text.append(f"Weight: {medical_record.weight} kg")
        if medical_record.heart_rate:
            vitals_text.append(f"Heart Rate: {medical_record.heart_rate} bpm")
        
        story.append(Paragraph("Vitals:", heading_style))
        story.append(Paragraph(" | ".join(vitals_text), normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Prescriptions
    story.append(Paragraph("Medications:", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    prescriptions = medical_record.prescriptions.all()
    
    if prescriptions.exists():
        rx_data = [['S.No', 'Medication', 'Dosage', 'Frequency', 'Duration']]
        
        for idx, rx in enumerate(prescriptions, 1):
            rx_data.append([
                str(idx),
                rx.medication_name,
                rx.dosage,
                rx.frequency,
                rx.duration
            ])
        
        rx_table = Table(rx_data, colWidths=[0.6*inch, 2.2*inch, 1.3*inch, 1.5*inch, 1.3*inch])
        rx_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(rx_table)
    else:
        story.append(Paragraph("No medications prescribed.", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Treatment plan
    if medical_record.treatment_plan:
        story.append(Paragraph("Treatment Plan:", heading_style))
        story.append(Paragraph(medical_record.treatment_plan, normal_style))
        story.append(Spacer(1, 0.15*inch))
    
    # Follow-up
    if medical_record.next_visit_date:
        story.append(Paragraph("Next Visit:", heading_style))
        story.append(Paragraph(
            medical_record.next_visit_date.strftime('%d-%B-%Y'),
            normal_style
        ))
    
    # Build PDF
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    
    buffer.seek(0)
    return buffer


# ============================================================================
# VACCINATION CERTIFICATE PDF
# ============================================================================

def generate_vaccination_pdf(vaccination):
    """Generate vaccination certificate PDF"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*inch,
        bottomMargin=2*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=BRAND_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=BRAND_COLOR,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Title
    story.append(Paragraph("VACCINATION CERTIFICATE", title_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Certificate number
    cert_para = Paragraph(
        f"<b>Certificate No:</b> {vaccination.certificate_number}",
        styles['Normal']
    )
    story.append(cert_para)
    story.append(Spacer(1, 0.3*inch))
    
    # Patient details
    patient = vaccination.patient
    patient_data = [
        ['Patient Name:', patient.pet_name],
        ['Species:', patient.species.capitalize()],
        ['Breed:', patient.breed or 'N/A'],
        ['Age:', patient.age_string],
        ['Owner Name:', patient.owner.name],
        ['Owner Phone:', patient.owner.phone],
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4.8*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Vaccination details
    story.append(Paragraph("Vaccination Details:", heading_style))
    
    vacc_data = [
        ['Vaccine Name:', vaccination.vaccine_name],
        ['Manufacturer:', vaccination.manufacturer or 'N/A'],
        ['Batch Number:', vaccination.batch_number or 'N/A'],
        ['Date Administered:', vaccination.date_administered.strftime('%d-%B-%Y')],
        ['Next Due Date:', vaccination.next_due_date.strftime('%d-%B-%Y') if vaccination.next_due_date else 'N/A'],
        ['Administered By:', vaccination.administered_by.get_full_name() if vaccination.administered_by else 'N/A'],
    ]
    
    vacc_table = Table(vacc_data, colWidths=[2.2*inch, 4.6*inch])
    vacc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(vacc_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Notes
    if vaccination.notes:
        story.append(Paragraph("Additional Notes:", heading_style))
        story.append(Paragraph(vaccination.notes, styles['Normal']))
    
    # Build
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    
    buffer.seek(0)
    return buffer


# ============================================================================
# HEALTH CERTIFICATE PDF
# ============================================================================

def generate_health_certificate_pdf(patient):
    """Generate general health certificate PDF"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*inch,
        bottomMargin=2*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=BRAND_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=BRAND_COLOR,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Title
    story.append(Paragraph("HEALTH CERTIFICATE", title_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Issue date
    story.append(Paragraph(
        f"<b>Issue Date:</b> {datetime.now().strftime('%d-%B-%Y')}",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Patient info
    patient_data = [
        ['Patient Name:', patient.pet_name],
        ['Species:', patient.species.capitalize()],
        ['Breed:', patient.breed or 'N/A'],
        ['Gender:', patient.get_gender_display()],
        ['Date of Birth:', patient.date_of_birth.strftime('%d-%B-%Y') if patient.date_of_birth else 'N/A'],
        ['Age:', patient.age_string],
        ['Microchip ID:', patient.microchip_id or 'N/A'],
        ['Owner Name:', patient.owner.name],
        ['Owner Address:', patient.owner.address or 'N/A'],
        ['Owner Phone:', patient.owner.phone],
    ]
    
    patient_table = Table(patient_data, colWidths=[2.2*inch, 4.6*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Health status
    story.append(Paragraph("Health Status:", heading_style))
    
    # Get latest medical record
    latest_record = patient.medical_records.first()
    
    if latest_record:
        health_text = f"""
        This is to certify that the above-mentioned animal was examined on 
        {latest_record.visit_date.strftime('%d-%B-%Y')} and found to be in good health 
        with no signs of contagious or infectious disease.
        """
        
        if latest_record.temperature:
            health_text += f"<br/><br/>Temperature: {latest_record.temperature}°F (Normal)"
        if latest_record.weight:
            health_text += f"<br/>Weight: {latest_record.weight} kg"
    else:
        health_text = "Patient records indicate regular health monitoring. No current health concerns noted."
    
    story.append(Paragraph(health_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Vaccination status
    story.append(Paragraph("Vaccination Status:", heading_style))
    
    recent_vaccinations = patient.vaccinations.order_by('-date_administered')[:5]
    
    if recent_vaccinations.exists():
        vacc_data = [['Vaccine', 'Date', 'Next Due']]
        
        for vacc in recent_vaccinations:
            vacc_data.append([
                vacc.vaccine_name,
                vacc.date_administered.strftime('%d-%b-%Y'),
                vacc.next_due_date.strftime('%d-%b-%Y') if vacc.next_due_date else 'N/A'
            ])
        
        vacc_table = Table(vacc_data, colWidths=[2.5*inch, 2*inch, 2.3*inch])
        vacc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(vacc_table)
    else:
        story.append(Paragraph("No vaccination records available.", styles['Normal']))
    
    # Build
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    
    buffer.seek(0)
    return buffer


# ============================================================================
# LAB REPORT PDF
# ============================================================================

def generate_lab_report_pdf(lab_test):
    """Generate lab test report PDF"""
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2*inch,
        bottomMargin=2*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=BRAND_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=BRAND_COLOR,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Title
    story.append(Paragraph("LABORATORY TEST REPORT", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Patient info
    patient = lab_test.patient
    patient_data = [
        ['Patient Name:', patient.pet_name, 'Species:', patient.species.capitalize()],
        ['Owner Name:', patient.owner.name, 'Age:', patient.age_string],
        ['Test Name:', lab_test.test_name, 'Test Type:', lab_test.test_type or 'N/A'],
    ]
    
    patient_table = Table(patient_data, colWidths=[1.5*inch, 2.2*inch, 1.2*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Test info
    test_info_data = [
        ['Ordered Date:', lab_test.ordered_date.strftime('%d-%B-%Y %I:%M %p')],
        ['Sample Collected:', lab_test.sample_collected_date.strftime('%d-%B-%Y %I:%M %p') if lab_test.sample_collected_date else 'N/A'],
        ['Result Date:', lab_test.result_date.strftime('%d-%B-%Y %I:%M %p') if lab_test.result_date else 'Pending'],
        ['Status:', lab_test.get_status_display()],
        ['Ordered By:', lab_test.ordered_by.get_full_name() if lab_test.ordered_by else 'N/A'],
        ['Performed By:', lab_test.performed_by.get_full_name() if lab_test.performed_by else 'N/A'],
    ]
    
    test_info_table = Table(test_info_data, colWidths=[2*inch, 4.8*inch])
    test_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(test_info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Results
    story.append(Paragraph("Test Results:", heading_style))
    
    if lab_test.result_values:
        result_data = [['Parameter', 'Value', 'Unit']]
        
        for param, value in lab_test.result_values.items():
            if isinstance(value, dict):
                result_data.append([param, str(value.get('value', 'N/A')), value.get('unit', '')])
            else:
                result_data.append([param, str(value), ''])
        
        result_table = Table(result_data, colWidths=[2.5*inch, 2.5*inch, 1.8*inch])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(result_table)
    else:
        story.append(Paragraph("Results pending or not available.", styles['Normal']))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Notes
    if lab_test.result_notes:
        story.append(Paragraph("Notes:", heading_style))
        story.append(Paragraph(lab_test.result_notes, styles['Normal']))
    
    # Build
    doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    
    buffer.seek(0)
    return buffer
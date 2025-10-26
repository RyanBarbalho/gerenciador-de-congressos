# PDF Generation Integration

## Overview

The PDF generation functionality has been successfully integrated into both the command-line interface (`main.py`) and the Streamlit web application (`streamlit_app.py`).

## Features

### 1. Automatic PDF Generation in main.py

After a successful allocation, the system automatically generates a PDF with the class schedules:

- **Output File**: `horario_alocacao.pdf`
- **Content**: One page per room showing all allocated classes with their schedules
- **Automatic**: Generates immediately after allocation completes

#### How it works:

```bash
python app/main.py
```

The system will:
1. Load data from CC and EC CSV files
2. Execute the allocation using linear programming
3. Display allocation results
4. **Automatically generate PDF** with the schedules
5. Display confirmation message with PDF location

#### Sample Output:

```
================================================================================
GERANDO PDF COM HORÁRIOS DE ALOCAÇÃO
================================================================================
✓ PDF gerado com sucesso: horario_alocacao.pdf
  - 45 alocações incluídas
  - 12 salas no documento
```

### 2. PDF Generation in Streamlit App

The Streamlit interface now has PDF generation capabilities in two locations:

#### A. After Allocation (⚙️ Alocação Page)

Right after executing an allocation:

1. Click "🚀 Executar Alocação"
2. When successful, a new section appears
3. Click "📄 Gerar PDF de Horários Agora"
4. Download the generated PDF

#### B. Results Page (📈 Resultados)

At the top of the Results page:

1. Button "📄 Gerar PDF de Horários" - Generate new PDF
2. Button "⬇️ Download PDF Existente" - Download previously generated PDF

Both buttons provide immediate download functionality.

## PDF Structure

The generated PDF includes:

- **Page per Room**: Each room gets its own page
- **Room Information**: 
  - Room name
  - Location (IC, IF, IM)
  - Capacity
  - Equipment type
- **Class Schedule Grid**:
  - Days of the week (Monday-Friday)
  - Time slots (M1-M6, T1-T6)
  - Color-coded classes
  - Course names and student counts
- **Visual Design**:
  - Professional landscape layout
  - Color-coded for easy reading
  - Automatic text sizing
  - Interval breaks marked

## Requirements

The PDF generation requires the `reportlab` library:

```bash
pip install reportlab
```

This is already included in `requirements_streamlit.txt`.

## Error Handling

The system gracefully handles PDF generation failures:

- **Missing reportlab**: Shows a warning but continues with allocation
- **Generation errors**: Displays error message without crashing
- **File access issues**: Provides clear error feedback

## Integration Points

### In main.py:

```python
try:
    from pdf_generator import create_timetable_pdf_from_alocacoes
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
```

### In streamlit_app.py:

```python
if PDF_AVAILABLE:
    if st.button("📄 Gerar PDF de Horários"):
        sucesso_pdf = create_timetable_pdf_from_alocacoes(resultado, "horario_alocacao.pdf")
```

## Output Examples

### Command Line Output:

```
horario_alocacao.pdf - Generated with 12 pages, one per room
```

### Streamlit Output:

Visual buttons with download capability directly in the browser.

## Technical Details

### pdf_generator.py Functions Used:

- `create_timetable_pdf_from_alocacoes(alocacoes_resultado, output_filename)`:
  - **Input**: AlocacaoResultado object
  - **Output**: PDF file (boolean success)
  - **Conversion**: Automatically converts allocation data to PDF format

### Data Flow:

```
Allocation Result (AlocacaoResultado)
    ↓
convert_alocacoes_to_pdf_format()
    ↓
Grouped by Room
    ↓
create_timetable_pdf_from_alocacoes()
    ↓
PDF File (horario_alocacao.pdf)
```

## Benefits

1. **Immediate Visualization**: See schedules right after allocation
2. **Professional Output**: Print-ready PDF for distribution
3. **Room-by-Room View**: Easy to post on room doors
4. **Color Coding**: Quick visual identification of classes
5. **Integrated Workflow**: No manual export needed

## Usage Examples

### Quick Start:

1. Run allocation: `python app/main.py`
2. Find PDF: `horario_alocacao.pdf` in project root

### Streamlit:

1. Navigate to ⚙️ Alocação page
2. Execute allocation
3. Click "Gerar PDF de Horários Agora"
4. Download appears automatically

## Customization

To change PDF filename in Streamlit:

```python
pdf_filename = "meu_horario.pdf"
create_timetable_pdf_from_alocacoes(resultado, pdf_filename)
```

## Troubleshooting

**Problem**: PDF not generating
- **Solution**: Check if reportlab is installed

**Problem**: PDF is empty
- **Solution**: Ensure allocation has results

**Problem**: Cannot download in Streamlit
- **Solution**: Check file permissions and browser settings

## Future Enhancements

Possible improvements:

- Custom PDF themes
- Multiple PDF formats (by course, by time slot)
- Email PDF directly
- PDF preview in Streamlit
- Batch PDF generation


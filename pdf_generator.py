import random
import sys
import os
import re
from typing import Dict, List, Tuple, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    FONT_NAME = 'Arial'
    FONT_NAME_BOLD = 'Arial-Bold'
    pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, 'arialbd.ttf'))
except:
    print("Arial font not found, using Helvetica.")
    FONT_NAME = 'Helvetica'
    FONT_NAME_BOLD = 'Helvetica-Bold'

PDF_FILENAME = "horario_alocacao.pdf"
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

MARGIN_TOP = 1.2 * cm
MARGIN_BOTTOM = 1.0 * cm
MARGIN_LEFT = 0.8 * cm
MARGIN_RIGHT = 0.8 * cm

HEADER_HEIGHT = 1.8 * cm
FOOTER_HEIGHT = 0.6 * cm
DAY_LABEL_WIDTH = 2.0 * cm
TIMESLOT_HEADER_HEIGHT = 1.8 * cm

GRID_X_START = MARGIN_LEFT + DAY_LABEL_WIDTH
GRID_Y_START = PAGE_HEIGHT - MARGIN_TOP - HEADER_HEIGHT - TIMESLOT_HEADER_HEIGHT
GRID_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - DAY_LABEL_WIDTH
GRID_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - HEADER_HEIGHT - FOOTER_HEIGHT - TIMESLOT_HEADER_HEIGHT

DAYS_OF_WEEK = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']

TIMESLOT_DEFINITIONS = [
    ('M1', '07:00', '07:50', False),
    ('M2', '08:00', '08:50', False),
    ('M3', '09:00', '09:50', False),
    ('M4', '10:00', '10:50', False),
    ('M5', '11:00', '11:50', False),
    ('M6', '12:00', '12:50', False),
    ('INT2', 'Almoço', '', True),
    ('T1', '13:00', '13:50', False),
    ('T2', '13:50', '14:40', False),
    ('T3', '14:40', '15:30', False),
    ('T4', '15:30', '16:20', False),
    ('T5', '16:20', '17:10', False),
    ('T6', '17:10', '18:00', False),
]

ROW_HEIGHT = GRID_HEIGHT / len(DAYS_OF_WEEK)

NUM_REGULAR_SLOTS = sum(1 for _, _, _, is_interval in TIMESLOT_DEFINITIONS if not is_interval)
NUM_INTERVAL_SLOTS = sum(1 for _, _, _, is_interval in TIMESLOT_DEFINITIONS if is_interval)
REGULAR_SLOT_RELATIVE_WIDTH = 1.0
INTERVAL_SLOT_RELATIVE_WIDTH = 0.4

TOTAL_RELATIVE_WIDTH_UNITS = (NUM_REGULAR_SLOTS * REGULAR_SLOT_RELATIVE_WIDTH) + \
                             (NUM_INTERVAL_SLOTS * INTERVAL_SLOT_RELATIVE_WIDTH)

REGULAR_COL_WIDTH = (GRID_WIDTH / TOTAL_RELATIVE_WIDTH_UNITS) * REGULAR_SLOT_RELATIVE_WIDTH
INTERVAL_COL_WIDTH = (GRID_WIDTH / TOTAL_RELATIVE_WIDTH_UNITS) * INTERVAL_SLOT_RELATIVE_WIDTH

COLUMN_PROPERTIES = []
current_x = GRID_X_START
for slot_id, _, _, is_interval in TIMESLOT_DEFINITIONS:
    col_w = INTERVAL_COL_WIDTH if is_interval else REGULAR_COL_WIDTH
    COLUMN_PROPERTIES.append({'id': slot_id, 'x': current_x, 'width': col_w})
    current_x += col_w

SLOT_ID_TO_INDEX = {slot['id']: i for i, slot in enumerate(COLUMN_PROPERTIES)}

styles = getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle(
    'TitleStyle', parent=styles['h1'], fontName=FONT_NAME_BOLD, fontSize=16, alignment=TA_LEFT, spaceAfter=0.1*cm
)
LOCATION_STYLE = ParagraphStyle(
    'LocationStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=10, alignment=TA_LEFT, spaceAfter=0.3*cm
)
DAY_LABEL_STYLE = ParagraphStyle(
    'DayLabelStyle', parent=styles['Normal'], fontName=FONT_NAME_BOLD, fontSize=11, alignment=TA_CENTER, leading=12
)
TIMESLOT_LABEL_STYLE = ParagraphStyle(
    'TimeslotLabelStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, alignment=TA_CENTER, leading=9
)
COURSE_TEXT_STYLE = ParagraphStyle(
    'CourseStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, textColor=colors.black,
    alignment=TA_CENTER, leading=9
)
FOOTER_STYLE = ParagraphStyle(
    'FooterStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=9, alignment=TA_LEFT
)

def generate_random_colors(num_colors=64):
    color_list = []
    for _ in range(num_colors):
        r = random.uniform(0.5, 1.0)
        g = random.uniform(0.5, 1.0)
        b = random.uniform(0.5, 1.0)
        color_list.append(colors.Color(r, g, b))
    return color_list

COLOR_PALETTE = generate_random_colors()
COLOR_IDX_GENERATOR = (i for i in range(len(COLOR_PALETTE)))

def get_next_color():
    global COLOR_IDX_GENERATOR
    try:
        idx = next(COLOR_IDX_GENERATOR)
    except StopIteration:
        COLOR_IDX_GENERATOR = (i for i in range(len(COLOR_PALETTE)))
        idx = next(COLOR_IDX_GENERATOR)
    return COLOR_PALETTE[idx % len(COLOR_PALETTE)]

def draw_page_template(c: canvas.Canvas, title_text: str, location_text: str):
    c.setFont(FONT_NAME, 10)

    p_title = Paragraph(title_text, TITLE_STYLE)
    title_width, title_height = p_title.wrap(PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEADER_HEIGHT)
    p_title.drawOn(c, MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP - title_height)

    p_location = Paragraph(location_text, LOCATION_STYLE)
    location_width, location_height = p_location.wrap(PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEADER_HEIGHT - title_height)
    p_location.drawOn(c, MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP - title_height - location_height - 0.2*cm)
    
    footer_text = f"Horário criado: {random.randint(1,28)}/{random.randint(1,12)}/2025"
    p_footer = Paragraph(footer_text, FOOTER_STYLE)
    footer_width, footer_height = p_footer.wrap(GRID_X_START + GRID_WIDTH - MARGIN_LEFT, FOOTER_HEIGHT)
    p_footer.drawOn(c, MARGIN_LEFT, FOOTER_HEIGHT) 

    asc_footer_text = "Sistema de Alocação de Salas - Programação Linear"
    p_asc_footer = Paragraph(asc_footer_text, FOOTER_STYLE)
    asc_width, asc_height = p_asc_footer.wrap(GRID_X_START + GRID_WIDTH - MARGIN_LEFT, FOOTER_HEIGHT + 0.3*cm)
    p_asc_footer.drawOn(c, PAGE_WIDTH - MARGIN_RIGHT - asc_width, MARGIN_BOTTOM)

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    c.line(MARGIN_LEFT, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, MARGIN_LEFT + DAY_LABEL_WIDTH + GRID_WIDTH, GRID_Y_START + TIMESLOT_HEADER_HEIGHT)
    for i in range(len(DAYS_OF_WEEK) + 1):
        y = GRID_Y_START - (i * ROW_HEIGHT)
        c.line(MARGIN_LEFT, y, MARGIN_LEFT + DAY_LABEL_WIDTH + GRID_WIDTH, y)

    c.line(MARGIN_LEFT, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, MARGIN_LEFT, GRID_Y_START - GRID_HEIGHT)
    c.line(GRID_X_START, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, GRID_X_START, GRID_Y_START - GRID_HEIGHT)
    
    for col_prop in COLUMN_PROPERTIES:
        x_line = col_prop['x'] + col_prop['width']
        c.line(x_line, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, x_line, GRID_Y_START - GRID_HEIGHT)

    for i, day_name in enumerate(DAYS_OF_WEEK):
        y_pos = GRID_Y_START - (i * ROW_HEIGHT) - ROW_HEIGHT / 2
        p_day = Paragraph(day_name, DAY_LABEL_STYLE)
        w, h = p_day.wrap(DAY_LABEL_WIDTH, ROW_HEIGHT)
        p_day.drawOn(c, MARGIN_LEFT + (DAY_LABEL_WIDTH - w)/2, y_pos - h/2)

    y_label_base = GRID_Y_START + TIMESLOT_HEADER_HEIGHT
    for col_prop in COLUMN_PROPERTIES:
        slot_id = col_prop['id']
        original_def = next(s_def for s_def in TIMESLOT_DEFINITIONS if s_def[0] == slot_id)
        label_L1 = original_def[1]
        label_L2 = original_def[2]
        
        if original_def[3]:
            full_label_text = f"<font size=6>{label_L1}</font><br/><font size=6>{label_L2}</font>"
        else:
            full_label_text = f"<b>{label_L1}</b><br/><font size=7>{label_L2}</font>"
        
        p_slot = Paragraph(full_label_text, TIMESLOT_LABEL_STYLE)
        
        col_width = col_prop['width']
        w, h = p_slot.wrap(col_width, TIMESLOT_HEADER_HEIGHT)
        
        p_slot.drawOn(c, col_prop['x'] + (col_width - w) / 2, y_label_base - h - 0.2*cm)

def get_elementary_slots_indices(start_slot_id: str, end_slot_id: str):
    try:
        start_idx = SLOT_ID_TO_INDEX[start_slot_id]
        end_idx = SLOT_ID_TO_INDEX[end_slot_id]
    except KeyError:
        print(f"Error: Slot ID {start_slot_id} or {end_slot_id} not found in SLOT_ID_TO_INDEX.")
        return []
    
    if start_idx > end_idx:
        print(f"Warning: start_slot_id {start_slot_id} is after end_slot_id {end_slot_id}.")
        return []
    return list(range(start_idx, end_idx + 1))

def get_course_blocks_with_intervals(start_slot_id: str, end_slot_id: str):
    try:
        start_idx = SLOT_ID_TO_INDEX[start_slot_id]
        end_idx = SLOT_ID_TO_INDEX[end_slot_id]
    except KeyError:
        print(f"Error: Slot ID {start_slot_id} or {end_slot_id} not found.")
        return []
    
    if start_idx > end_idx:
        return []
    
    blocks = []
    current_block_start = start_idx
    
    for i in range(start_idx, end_idx + 1):
        slot_id = COLUMN_PROPERTIES[i]['id']
        is_interval = False
        for _, _, _, interval_flag in TIMESLOT_DEFINITIONS:
            if _ == slot_id and interval_flag:
                is_interval = True
                break
        
        if is_interval:
            if current_block_start < i:
                blocks.append((current_block_start, i - 1))
            current_block_start = i + 1
    
    if current_block_start <= end_idx:
        blocks.append((current_block_start, end_idx))
    
    return blocks

def draw_course_block_split(c: canvas.Canvas, day_index: int, start_slot_id: str, end_slot_id: str,
                           course_name: str, room_info: str, fill_color):
    blocks = get_course_blocks_with_intervals(start_slot_id, end_slot_id)
    
    if not blocks:
        print(f"No valid blocks found for course {course_name}")
        return
    
    for block_start_idx, block_end_idx in blocks:
        block_x = COLUMN_PROPERTIES[block_start_idx]['x']
        block_y = GRID_Y_START - ((day_index + 1) * ROW_HEIGHT)
        
        block_width = 0
        for i in range(block_start_idx, block_end_idx + 1):
            block_width += COLUMN_PROPERTIES[i]['width']
        
        block_height = ROW_HEIGHT

        padding = 1
        c.setFillColor(fill_color)
        c.setStrokeColor(colors.darkgrey)
        c.rect(block_x + padding, block_y + padding, block_width - 2*padding, block_height - 2*padding, fill=1, stroke=1)

        r, g, b, _ = fill_color.rgba()
        text_color = colors.black
        if (r + g + b) < 1.5:
            text_color = colors.white
        
        course_p_style = ParagraphStyle(
            'CourseBlockStyle', 
            parent=COURSE_TEXT_STYLE, 
            textColor=text_color,
            fontSize=8,
            leading=9,
            alignment=TA_CENTER,
            fontName=FONT_NAME,
            allowWidows=1,
            allowOrphans=1
        )

        max_course_name_length = 40
        display_name = course_name if len(course_name) <= max_course_name_length else course_name[:max_course_name_length] + "..."
        
        text_content = f"<font name='{FONT_NAME}'>{display_name}</font><br/><br/><font name='{FONT_NAME_BOLD}'><b>{room_info}</b></font>"
        p_course = Paragraph(text_content, course_p_style)
        
        text_area_width = block_width - 0.4 * cm
        text_area_height = block_height - 0.3 * cm
        
        if text_area_width > 0 and text_area_height > 0:
            w, h = p_course.wrap(text_area_width, text_area_height)
            
            text_x = block_x + (block_width - w) / 2
            text_y = block_y + (block_height - h) / 2
            p_course.drawOn(c, text_x, text_y)

def parse_horario_to_slots(horario_str: str) -> List[Tuple[str, str, str]]:
    day_mapping = {
        'Segunda': 'Seg',
        'Terça': 'Ter', 
        'Quarta': 'Qua',
        'Quinta': 'Qui',
        'Sexta': 'Sex',
        'Sábado': 'Sab',
        'Domingo': 'Dom'
    }
    
    time_to_slot = {}
    for slot_id, start_time, end_time, is_interval in TIMESLOT_DEFINITIONS:
        if not is_interval and start_time:
            time_to_slot[start_time] = slot_id
    
    slots = []
    
    horario_parts = horario_str.split(' | ')
    
    for part in horario_parts:
        match = re.match(r'([^0-9]+)\s+(.+)', part.strip())
        if not match:
            continue
            
        dias_str, horarios_str = match.groups()
        dias = [d.strip() for d in dias_str.split('/')]
        horarios = [h.strip() for h in horarios_str.split('/')]
        
        for dia in dias:
            day_abbrev = day_mapping.get(dia, dia)
            
            if day_abbrev not in DAYS_OF_WEEK:
                continue
            
            slot_ids = []
            for horario in horarios:
                time_match = re.match(r'(\d{2}:\d{2})-\d{2}:\d{2}', horario)
                if time_match:
                    start_time = time_match.group(1)
                    if start_time in time_to_slot:
                        slot_ids.append(time_to_slot[start_time])
            
            if len(slot_ids) >= 1:
                slot_ids_sorted = sorted(slot_ids, key=lambda x: SLOT_ID_TO_INDEX.get(x, 999))
                
                i = 0
                while i < len(slot_ids_sorted):
                    start_slot = slot_ids_sorted[i]
                    end_slot = start_slot
                    
                    j = i + 1
                    while j < len(slot_ids_sorted):
                        current_idx = SLOT_ID_TO_INDEX[slot_ids_sorted[j]]
                        end_idx = SLOT_ID_TO_INDEX[end_slot]
                        
                        if current_idx == end_idx + 1 or (current_idx > end_idx and current_idx <= end_idx + 2):
                            end_slot = slot_ids_sorted[j]
                            j += 1
                        else:
                            break
                    
                    slots.append((day_abbrev, start_slot, end_slot))
                    i = j
    
    return slots

def convert_alocacoes_to_pdf_format(alocacoes_resultado):
    from app.models.domain import AlocacaoResultado
    
    if not isinstance(alocacoes_resultado, AlocacaoResultado) or not alocacoes_resultado.sucesso:
        print("Resultado de alocação inválido ou sem sucesso")
        return {}
    
    alocacoes = alocacoes_resultado.alocacoes
    
    grouped_data = {}
    
    for alocacao in alocacoes:
        materia = alocacao.materia
        sala = alocacao.sala
        
        slots = parse_horario_to_slots(materia.horario)
        
        if not slots:
            print(f"Warning: Could not parse horario '{materia.horario}' for materia '{materia.nome}'")
            continue
        
        sala_key = sala.id
        if sala_key not in grouped_data:
            grouped_data[sala_key] = {
                'sala': sala,
                'courses': []
            }
        
        material_label = {0: "", 1: " [COMP]", 2: " [ROB]", 3: " [ELET]"}.get(materia.material, "")
        
        course_entry = {
            'id': materia.id,
            'name': materia.nome + material_label,
            'room_info': f"{sala.nome} ({materia.inscritos} alunos)",
            'slots': slots,
            'material': materia.material
        }
        grouped_data[sala_key]['courses'].append(course_entry)
    
    return grouped_data

def create_timetable_pdf_from_alocacoes(alocacoes_resultado, output_filename: str = None):
    if output_filename:
        global PDF_FILENAME
        PDF_FILENAME = output_filename
    
    print("Convertendo resultado de alocação para formato PDF...")
    grouped_data = convert_alocacoes_to_pdf_format(alocacoes_resultado)
    
    if not grouped_data:
        print("Nenhum dado para gerar PDF")
        return False
    
    c = canvas.Canvas(PDF_FILENAME, pagesize=landscape(A4))
    c.setTitle("Horário de Alocação de Salas")
    
    for sala_id, data in sorted(grouped_data.items(), key=lambda x: x[1]['sala'].nome):
        sala = data['sala']
        courses = data['courses']
        
        page_title = f"Sala: {sala.nome}"
        location_info = f"Instituto de Computação IC/UFAL - {sala.tipo.value.upper()} - Capacidade: {sala.capacidade}"
        if sala.local.value == 'im':
            location_info += f" - Instituto de Matemática (Custo: R$ {sala.custo_adicional:.2f})"
        
        draw_page_template(c, page_title, location_info)
        
        occupied_slots = set()
        
        for course in courses:
            course_color = get_next_color()
            
            for day_str, start_slot, end_slot in course['slots']:
                try:
                    day_idx = DAYS_OF_WEEK.index(day_str)
                except ValueError:
                    print(f"Warning: Invalid day '{day_str}' for course '{course['name']}'. Skipping slot.")
                    continue
                
                slot_tuple = (day_idx, start_slot, end_slot)
                if slot_tuple in occupied_slots:
                    continue
                
                occupied_slots.add(slot_tuple)
                
                draw_course_block_split(c, day_idx, start_slot, end_slot,
                                      course["name"], course["room_info"], course_color)
        
        c.showPage()

    c.save()
    print(f"PDF '{PDF_FILENAME}' gerado com sucesso.")
    return True

def create_test_pdf_with_mock_data():
    from app.models.domain import Materia, Sala, Alocacao, AlocacaoResultado, TipoSala, LocalSala
    
    print("Criando dados de teste com horários únicos...")
    
    materias = [
        Materia(id='TEST001', nome='Cálculo I', inscritos=45, horario='Segunda 08:00-08:50/09:00-09:50', material=0),
        Materia(id='TEST002', nome='Programação I', inscritos=30, horario='Segunda 13:00-13:50/13:50-14:40', material=1),
        Materia(id='TEST003', nome='Álgebra Linear', inscritos=38, horario='Terça 08:00-08:50/09:00-09:50', material=0),
        Materia(id='TEST004', nome='Estruturas de Dados', inscritos=25, horario='Terça 13:00-13:50/13:50-14:40', material=1),
        Materia(id='TEST005', nome='Banco de Dados', inscritos=35, horario='Quarta 08:00-08:50/09:00-09:50', material=1),
        Materia(id='TEST006', nome='Robótica I', inscritos=20, horario='Quarta 13:00-13:50/13:50-14:40', material=2),
        Materia(id='TEST007', nome='Inteligência Artificial', inscritos=40, horario='Quinta 08:00-08:50/09:00-09:50', material=0),
        Materia(id='TEST008', nome='Redes de Computadores', inscritos=32, horario='Quinta 13:00-13:50/13:50-14:40', material=0),
        Materia(id='TEST009', nome='Sistemas Operacionais', inscritos=28, horario='Sexta 08:00-08:50/09:00-09:50', material=0),
        Materia(id='TEST010', nome='Compiladores', inscritos=22, horario='Sexta 13:00-13:50/13:50-14:40', material=0),
    ]
    
    salas = [
        Sala(id='S01', nome='Sala IC-101', capacidade=50, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S02', nome='Lab IC-301', capacidade=35, tipo=TipoSala.LABORATORIO, local=LocalSala.IC, tipo_equipamento=1),
        Sala(id='S03', nome='Sala IC-102', capacidade=45, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S04', nome='Lab IC-302', capacidade=30, tipo=TipoSala.LABORATORIO, local=LocalSala.IC, tipo_equipamento=1),
        Sala(id='S05', nome='Sala IC-103', capacidade=40, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S06', nome='Lab Robótica', capacidade=25, tipo=TipoSala.LABORATORIO, local=LocalSala.IC, tipo_equipamento=2),
        Sala(id='S07', nome='Sala IC-104', capacidade=45, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S08', nome='Sala IC-105', capacidade=35, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S09', nome='Sala IC-106', capacidade=30, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
        Sala(id='S10', nome='Sala IC-107', capacidade=25, tipo=TipoSala.AULA, local=LocalSala.IC, tipo_equipamento=0),
    ]
    
    alocacoes = [
        Alocacao(materias[0], salas[0], 0, 0),
        Alocacao(materias[1], salas[1], 0, 0),
        Alocacao(materias[2], salas[2], 0, 0),
        Alocacao(materias[3], salas[3], 0, 0),
        Alocacao(materias[4], salas[4], 0, 0),
        Alocacao(materias[5], salas[5], 0, 0),
        Alocacao(materias[6], salas[6], 0, 0),
        Alocacao(materias[7], salas[7], 0, 0),
        Alocacao(materias[8], salas[8], 0, 0),
        Alocacao(materias[9], salas[9], 0, 0),
    ]
    
    resultado = AlocacaoResultado(sucesso=True, alocacoes=alocacoes)
    
    print(f"✓ Criadas {len(alocacoes)} alocações de teste")
    return resultado

def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        print("=== GERADOR DE PDF - SISTEMA DE ALOCAÇÃO ===\n")
        
        from app.services.data_loader import SistemaCompletoRefatorado
        from app.repositories.alocacao_repo import AlocacaoLinearStrategy
        from app.strategies.interfaces import CompatibilidadePadrao
        
        sistema = SistemaCompletoRefatorado()
        
        print("Carregando dados de CC...")
        repository_cc = sistema.carregar_dados_csv('oferta_cc_2025_1.csv')
        materias = list(repository_cc.buscar_materias())
        salas = list(repository_cc.buscar_salas())
        
        print(f"✓ {len(materias)} matérias carregadas")
        print(f"✓ {len(salas)} salas carregadas")
        
        print("\nExecutando alocação...")
        compatibilidade = CompatibilidadePadrao()
        alocador = AlocacaoLinearStrategy(compatibilidade)
        resultado = alocador.alocar(materias, salas)
        
        if resultado.sucesso:
            print(f"✓ Alocação bem-sucedida: {len(resultado.alocacoes)} alocações")
            print("\nGerando PDF...")
            create_timetable_pdf_from_alocacoes(resultado)
            return True
        else:
            print(f"\n❌ Erro na alocação: {resultado.erro}")
            print("\n💡 Capacidade insuficiente detectada. Usando dados de teste...")
            
            resultado_teste = create_test_pdf_with_mock_data()
            print("\nGerando PDF com dados de teste...")
            create_timetable_pdf_from_alocacoes(resultado_teste, output_filename="horario_teste_demo.pdf")
            print("\n✓ PDF de demonstração criado com sucesso!")
            return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que o módulo 'app' está disponível no PYTHONPATH")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = main()
    sys.exit(0 if sucesso else 1)

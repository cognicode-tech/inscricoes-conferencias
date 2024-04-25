import time
from h2o_wave import main, app, Q, ui, on, run_on 

@on('#conferencias-inicio')
async def conferencias_inicio(q: Q):
    q.page['sidebar'].value = '#conferencias-inicio'
    q.page['form'] = ui.form_card(
        box='vertical',
        items=[ui.link(name='add_conference_button',label='Nova Conferência',path='#conferencias-registro',target='_self',button=True),
            ui.table(
                name="table_history",
                columns=[
                    ui.table_column(name='table_name', label='Nome',max_width='350px',link=False),
                    ui.table_column(name='table_data', label='Data'),
                    ui.table_column(name='table_local', label='Local'),
                    ui.table_column(name='actions',max_width='50px',label='Ações',align='left',cell_type=ui.menu_table_cell_type(
                            name='commands',
                            commands=[
                                ui.command(name='reload_row', label='Editar'),
                                ui.command(name='delete_row', label='Deletar'),
                            ])),
                ],
                rows=[ui.table_row(name=r.id, cells=[r.name, r.data, r.local]) for r in q.client.rows] if q.client.rows is not None else []  
            )])

async def start_page(q: Q):
    q.page['sidebar'].value = '#conferencias-inicio'

    q.page['title'] = ui.text(name='', content='')
    q.page['form'] = ui.form_card(box='vertical', items=[
        #ui.button (name='button', label='Nova Conferência', icon='CirclePlus', primary=True, path='#conferencias-registro'),
        ui.link(name='add_conference_button', label='Nova Conferência', path='#conferencias-registro', target='_self', button=True)
    ])

@on('#conferencias-registro')
async def conferencias_registro(q: Q):
    q.page['sidebar'].value = '#conferencias-registro'
    clear_cards(q)

    q.page['title'] = ui.form_card(box='vertical', items=[
        ui.inline(justify='between', items=[
            ui.text_xl(name='title_conf', content='Conferências'),
            ui.button (name='button_sup', icon='AddPhone',label='Suporte', path='#PLACEHOLDER'),
        ]),
    ])

    q.page['form'] = ui.form_card(box='vertical', items=[
        ui.text_xl(name='register_conf_title', content='Nova Conferência'),
        ui.text_s(name='register_conf_subtitle', content='Preencha os detalhes do evento'),
        ui.textbox(name='conf_name_register_textbox', label='Nome'),
        ui.date_picker(name='conf_date_register_picker', label='Date'),
        ui.textbox(name='conf_city_register_textbox', label='Local'),
        ui.text_xl(name='space-text', content=''),
        ui.inline(justify='center', items=[
            ui.button (name='button_conference_register', label='Criar Conferência', icon='AcceptMedium', primary=True)
        ]),
    ])

@on('#conferencias-inscricoes') 
async def conferencias_inscricao(q: Q):
    q.page['sidebar'].value = '#conferencias-inscricoes'
    clear_cards(q)
    
    q.page['title'] = ui.text(name='', content='')
    q.page['form'] = ui.form_card(box='horizontal', items = [ 
        ui.text_xl(name='register_title', content='Nova Inscrição'),
        ui.text_s(name='register_subtitle', content='Preencha os detalhes da inscrição'),
        ui.textbox(name='conf_textbox', label='Conferência', placeholder='Conferência...'),
        ui.inline(justify='between', items=[ 
            ui.textbox(name='resp_textbox', label='Responsável', placeholder='Responsável...',width='400px'),
            ui.textbox(name='city_textbox', label='Cidade', placeholder='Local...',width='400px'),
            ui.textbox(name='Estate', label='Estado', placeholder='Estado...',width='400px'),
        ]),
        ui.inline(justify='between', items=[
            ui.textbox(name='pay-paper_textbox', label='Pg. Dinheiro', placeholder='0.00',width='300px'),
            ui.textbox(name='pay-deposit_textbox', label='Pg. Depósito', placeholder='0.00',width='300px'),
            ui.textbox(name='pay-transfer_textbox', label='Pg. Transferência', placeholder='0.00',width='300px'),
            ui.textbox(name='pay-check_textbox', label='Pg. Cheque', placeholder='0.00',width='300px'),
        ]),
        ui.inline(justify='between', items=[
            ui.textbox(name='total-pay_textbox', label='Pg. Total', placeholder='0.00',width='300px', disabled=True),
            ui.textbox(name='total-register_textbox', label='Total inscrições', placeholder='0.00',width='300px', disabled=True),
            ui.textbox(name='pendent-pay_textbox', label='Pendências', placeholder='0.00',width='300px', disabled=True),
        ]),
        ui.textbox(name='textbox_register', label='Observações',placeholder='Observações',height='100px' ,multiline=True),
        ui.text_xl(name='space_text', content='----'),
        ui.text_xl(name='participants_text', content='Participantes'),
        ui.button (name='button', label='Adicionar Participante', icon='AcceptMedium'),
        ui.inline(justify='between', items=[
            ui.textbox(name='register-name_textbox', label='Nome', width='300px'),
            ui.textbox(name='register-age_textbox', label='Idade', width='150px'),
            ui.dropdown(name='register-gender', label='Gender', placeholder='Selecione', 
            choices=[
                ui.choice(name='gender-M', label='M'),
                ui.choice(name='gender-F', label='F'),
            ],
            width='300px',
            ),
            ui.textbox(name='pay_textbox', label='Valor', placeholder='0.00',width='300px'),
        ]),
        ui.text_xl(name='space-text_2', content='----'),
        ui.inline(justify='center', items=[
            ui.button (name='button', label='Adicionar Participante', icon='AcceptMedium', primary=True),
        ]),
    ])

def clear_cards(q: Q):
    del q.page['title']
    del q.page['form']

class ConferenceList:
    _id = 0

    def __init__(self, name, date, local):
        ConferenceList._id += 1
        self.id = f'row_{ConferenceList._id}'
        self.name = name
        self.data = date
        self.local = local
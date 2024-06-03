from h2o_wave import main, app, Q, ui, on, run_on

# Utilities
from inscricoes.utilities.utils import (add_card, clear_cards, 
                                        utils_get_multiple_conferences)

@on('#conferencias-inicio')
async def conferencias_inicio(q: Q):
    q.page['sidebar'].value = '#conferencias-inicio'
    clear_cards(q)
    
    add_card(
        q, 
        'main_conference_button', 
        ui.form_card(box='horizontal', items=[
            ui.link(name='new_conference_link', label='Nova Conferência', path='#conferencias-registro', target='_self', button=True)
            ]
        )
    )
    
    await conferencias_inicio_table(q, conferences=utils_get_multiple_conferences())

# Update the Main Page Table
async def conferencias_inicio_table(q: Q, conferences):
    return add_card(
        q, 
        'main_conference_table',
        ui.form_card(
            ui.box('vertical'), 
            items=[
                ui.table(
                    name="main_table_list",
                    single=True,
                    checkbox_visibility='hidden',
                    columns=[
                        ui.table_column(name='main_conference_table_name', label='Nome',max_width='350px',link=False),
                        ui.table_column(name='main_conference_table_data', label='Data', link=False),
                        ui.table_column(name='main_conference_table_local', label='Local',link=False),
                        ui.table_column(name='main_conference_table_actions',max_width='50px',label='Ações',align='left',link=False, 
                            cell_type=ui.menu_table_cell_type(
                            name='commands',
                            commands=[
                                ui.command(name='main_conference_edit_table_row', label='Editar'),
                                ui.command(name='main_conference_delete_table_row', label='Deletar'),
                                ]
                            )
                        ),
                    ],
                    rows=[ui.table_row(name=str(r.id), cells=[r.nome, r.data, r.local]) for r in conferences] if conferences is not None else []
                )
            ]
        )
    )

@on('#conferencias-registro')
async def conferencias_registro(q: Q):
    q.page['sidebar'].value = '#conferencias-registro'
    clear_cards(q)
    
    add_card(
        q, 
        'top_support_section',
        ui.form_card(
            ui.box('horizontal'), 
            items=[
                ui.inline(justify='between', items=[
                    ui.text_xl(name='support_title', content='Conferências'),
                    ui.button (name='support_button', icon='AddPhone',label='Suporte', path='#PLACEHOLDER'),
                    ]
                )
            ]
        )
    )
    
    add_card(
        q, 
        'new_conference_form',
        ui.form_card(
            ui.box('vertical'), 
            items=[
                ui.text_xl(name='new_conference_title', content='Nova Conferência'),
                ui.text_s(name='new_conference_subtitle', content='Preencha os detalhes do evento'),
                ui.textbox(name='new_conference_name', label='Nome'),
                ui.date_picker(name='new_conference_date', label='Data'),
                ui.textbox(name='new_conference_city', label='Local'),
                ui.text_xl(name='new_conference_space_text', content=''),
                ui.inline(justify='center', 
                    items=[
                        ui.button (name='new_conference_button', label='Criar Conferência', icon='AcceptMedium', primary=True)
                    ]
                )
            ]
        )
    )

@on('#conferencias-inscricoes') 
async def conferencias_inscricao(q: Q):
    q.page['sidebar'].value = '#conferencias-inscricoes'
    clear_cards(q)
    
    add_card(
        q,
        'conference_registrations',
        ui.form_card(
            ui.box('horizontal'),
            items=[
                ui.text_xl(name='register_title', content='Nova Inscrição'),
                ui.text_s(name='register_subtitle', content='Preencha os detalhes da inscrição'),
                ui.dropdown(name='register_select_conference',label='Conferência', placeholder='Selecione a conferência...',
                    choices=[
                        ui.choice(name=str(conf.id), label=conf.nome) for conf in utils_get_multiple_conferences()
                    ]   
                ),
                ui.inline(justify='between', items=[ 
                    ui.textbox(name='register_responsable', label='Responsável', placeholder='Responsável...',width='300px'),
                    ui.textbox(name='register_city', label='Cidade', placeholder='Local de origem...',width='300px'),
                    ui.textbox(name='register_estate', label='Estado', placeholder='Estado de origem...',width='300px'),
                    ]
                ),
                ui.inline(justify='between', items=[
                    ui.textbox(name='register_pay_paper', label='Pg. Dinheiro', placeholder='0.00',width='200px'),
                    ui.textbox(name='register_pay_deposit', label='Pg. Depósito', placeholder='0.00', width='200px'),
                    ui.textbox(name='register_pay_transfer', label='Pg. Transferência', placeholder='0.00', width='200px'),
                    ui.textbox(name='register_pay_check', label='Pg. Cheque', placeholder='0.00', width='200px'),
                    ]
                ),
                
                ui.textbox(name='register_observations', label='Observações',placeholder='Observações',height='80px' ,multiline=True)
            ]
        )
    )
    
    await conferencia_inscricoes_values(q)
    await conferencias_inscricao_table(q)
    
    add_card(
        q,
        'new_registration_button',
        ui.form_card(
            ui.box('vertical'),
            items=[
                ui.inline(justify='center', items=[
                    ui.button (name='submit_conference_registration_button', label='Criar Inscrição', icon='AcceptMedium', primary=True),
                    ]
                ),
            ]
        )
    )

async def conferencias_inscricao_table(q: Q):
    return add_card(
        q,
        'participant_registrations_table',
        ui.form_card(
            ui.box('vertical'),
            items=[
                ui.text_xl(name='participant_space_text', content=''),
                ui.text_xl(name='participant_text', content='Participantes'),
                ui.button(name='participant_add_button', label='Adicionar Participante', icon='AddTo', primary=True),
                ui.table(
                    name="participant_table_history",
                    single=True,
                    checkbox_visibility='hidden',
                    columns=[
                        ui.table_column(name='participant_table_name', label='Nome',max_width='350px',link=False),
                        ui.table_column(name='participant_table_idade', label='Idade'),
                        ui.table_column(name='participant_table_Sex', label='Sexo'),
                        ui.table_column(name='participant_table_type', label='Tipo de inscrição'),
                        ui.table_column(name='participant_table_value', label='Valor'),
                        ui.table_column(name='participant_table_actions',max_width='50px',label='Ações',align='left',cell_type=ui.menu_table_cell_type(
                            name='commands',
                            commands=[
                                ui.command(name='participant_edit_row', label='Editar'),
                                ui.command(name='participant_delete_row', label='Deletar')
                                ]
                            )
                        )
                    ],
                    rows=[ui.table_row(name=str(r.id), cells=[r.name, r.age, r.gender, r.type_register, f'R$ {r.value}' if r.type_register != 'Isento' else 'R$ 0.0']) for r in q.client.participant_list] if q.client.participant_list is not None else []
                ),
            ]
        )
    )
    
async def conferencia_inscricoes_values(q: Q):
    return add_card(
        q,
        'participant_registration_values',
        ui.form_card(
            ui.box('vertical'),
            items=[
                ui.inline(justify='between', items=[
                    ui.textbox(name='register_total_pay', label='Pg. Total', placeholder='0.00', value=q.client.register_total_pay, width='300px', readonly=True),
                    ui.textbox(name='register_total_people', label='Total inscrições', placeholder='0', value=q.client.register_total_people, width='300px', readonly=True),
                    ui.textbox(name='register_pendent_pay', label='Pendências', placeholder='0.00', width='300px', readonly=True),
                    ]
                ),
            ]
        )
    )


async def setup_app_layout(q: Q):
    conference_list=utils_get_multiple_conferences()
    
    q.page['sidebar'].value = '#conferencias-inicio'
    clear_cards(q)

    add_card(
        q, 
        'new_conference_button', 
        ui.form_card(box='horizontal', items=[
            ui.link(name='link_button', label='Nova Conferência', path='#conferencias-registro', target='_self', button=True)
            ]
        )
    )
    add_card(
        q, 
        'main_conference_table',
        ui.form_card(
            ui.box('vertical'), 
            items=[
                ui.table(
                    name="main_table_conf_list",
                    single=True,
                    checkbox_visibility='hidden',
                    columns=[
                        ui.table_column(name='conference_table_name', label='Nome',max_width='350px',link=False),
                        ui.table_column(name='conference_table_data', label='Data', link=False),
                        ui.table_column(name='conference_table_local', label='Local',link=False),
                        ui.table_column(name='conference_table_actions',max_width='50px',label='Ações',align='left',link=False, 
                            cell_type=ui.menu_table_cell_type(
                            name='commands',
                            commands=[
                                ui.command(name='main_conference_edit_table_row', label='Editar'),
                                ui.command(name='main_conference_delete_table_row', label='Deletar'),
                                ]
                            )
                        ),
                    ],
                    rows=[ui.table_row(name=str(r.id), cells=[r.nome, r.data, r.local]) for r in conference_list] if conference_list is not None else []
                    #rows=[ui.table_row(name=str(r.id), cells=[r.nome, r.data, r.local]) for r in read_multiple_conferences()] if read_multiple_conferences() is not None else []
                )
            ]
        )
    )
    
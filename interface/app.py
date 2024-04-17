from h2o_wave import main, app, Q, ui, on, run_on, data
from typing import Optional, List

def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q, ignore: Optional[List[str]] = []) -> None:
    if not q.client.cards:
        return

    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)

# Alterei alguns botões para 'link' para abrir na mesma aba, estou buscando uma forma de trocar a cor dele, ainda não achei na documentação
@on('#conferencias-inicio')
async def page_conferencias_inicio(q: Q):
    q.page['sidebar'].value = '#conferencias-inicio'
    clear_cards(q)

    add_card(q, 'button', ui.form_card(box='horizontal', items=[
        #ui.button (name='button', label='Nova Conferência', icon='CirclePlus', primary=True, path='#conferencias-registro'),
        ui.link(name='link_button', label='Nova Conferência', path='#conferencias-registro', target='_self', button=True)
    ]))

    commands = [
        ui.command(name='details', label='Details', icon='Info'),
        ui.command(name='delete', label='Delete', icon='Delete'),
    ]

    add_card(q, 'table', ui.form_card(box='vertical', items=[
    ui.table(
        name='table',
        columns=[
            ui.table_column(name='name', label='Nome', max_width='450px'),
            ui.table_column(name='data', label='Data', max_width='250px'),
            ui.table_column(name='location', label='Local', max_width='250px'),
            ui.table_column(name='actions', label='Ações', cell_type=ui.menu_table_cell_type(name='commands', commands=commands))
        ], 
        rows=[
            ui.table_row(name='row1', cells=['Test 1', '16/04/2024', 'Castanhal']),
            ui.table_row(name='row2', cells=['Test 2', '17/04/2024', 'Belém']),
            ui.table_row(name='row3', cells=['Test 3', '18/04/2024', 'Santarém']),
        ],)
    ]))

# O date_picker está em inglês, e ainda não encontrei meios de transformar ele para português ou apenas numeros.
@on('#conferencias-registro')
async def page_conferencias_inscricao(q: Q):
    q.page['sidebar'].value = '#conferencias-registro'
    clear_cards(q)

    add_card(q, 'button', ui.form_card(box='vertical', items=[
        ui.inline(justify='between', items=[
            ui.text_xl(name='title_conf', content='Conferências'),
            ui.button (name='button_sup', icon='AddPhone',label='Suporte', path='#page4'),
        ]),
    ]))

    add_card(q, 'form', ui.form_card(box='vertical', items = [ 
        ui.text_xl(name='register_conf_title', content='Nova Conferência'),
        ui.text_s(name='register_conf_subtitle', content='Preencha os detalhes do evento'),
        ui.textbox(name='conf_name_register_textbox', label='Nome'),
        ui.date_picker(name='conf_date_register_picker', label='Date'),
        ui.textbox(name='conf_city_register_textbox', label='Local'),
        ui.text_xl(name='space-text', content=''),
        ui.inline(justify='center', items=[
            #ui.button (name='button', label='Criar Conferência', icon='AcceptMedium', primary=True),
            ui.link(name='link_button', label='Nova Conferência', path='#conferencias-inicio', target='_self', button=True)
        ]),
    ])) 

@on('#conferencias-inscricao') 
async def conferencias_inscricao(q: Q):
    q.page['sidebar'].value = '#conferencias-inscricao'
    clear_cards(q) 
 
    add_card(q, 'form', ui.form_card(box='horizontal', items = [ 
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
    ]))   

@on('#conferencias-relatorios')
async def conferencias_relatorios(q: Q):
    q.page['sidebar'].value = '#conferencias-relatorios'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    add_card(q, 'form', ui.form_card(box='horizontal', items = [
        ui.text_xl(name='reports', content='Relatórios'),
    ]))

    for i in range(12):
        add_card(q, f'item{i}', ui.wide_info_card(box=ui.box('grid', width='400px'), name='', icon='ReportWarning', title=f'Conferencia {i+1}', caption='Lorem ipsum dolor sit amet'))

@on('#duvidas')
@on('duvidas_reset')
async def duvidas(q: Q):
    q.page['sidebar'].value = '#duvidas'
    clear_cards(q, ['form'])

    add_card(q, 'form', ui.form_card(box='vertical', items=[
        ui.stepper(name='stepper', items=[
            ui.step(label='Step 1'),
            ui.step(label='Step 2'),
            ui.step(label='Step 3'),
        ]),
        ui.textbox(name='textbox1', label='Textbox 1'),
        ui.buttons(justify='end', items=[
            ui.button(name='page4_step2', label='Next', primary=True),
        ]),
    ]))

@on()
async def duvidas_step2(q: Q):
    # Just update the existing card, do not recreate.
    q.page['form'].items = [
        ui.stepper(name='stepper', items=[
            ui.step(label='Step 1', done=True),
            ui.step(label='Step 2'),
            ui.step(label='Step 3'),
        ]),
        ui.textbox(name='textbox2', label='Textbox 2'),
        ui.buttons(justify='end', items=[
            ui.button(name='page4_step3', label='Next', primary=True),
        ])
    ]

@on()
async def duvidas_step3(q: Q):
    # Just update the existing card, do not recreate.
    q.page['form'].items = [
        ui.stepper(name='stepper', items=[
            ui.step(label='Step 1', done=True),
            ui.step(label='Step 2', done=True),
            ui.step(label='Step 3'),
        ]),
        ui.textbox(name='textbox3', label='Textbox 3'),
        ui.buttons(justify='end', items=[
            ui.button(name='page4_reset', label='Finish', primary=True),
        ])
    ]

@on('#sair')
async def sair(q: Q):
    q.page['sidebar'].value = '#sair'
    clear_cards(q)

    add_card(q, 'button', ui.form_card(box='horizontal', items=[
        ui.link(name='exit_button', label='Retornar', path='#conferencias-inicio', target='_self', button=True)
    ]))
    
async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', theme='solarized', title='Conferências',icon='AddGroup', layouts=[ui.layout( breakpoint='xs', min_height='100vh', zones=[
        ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
            ui.zone('sidebar', size='250px'),
            ui.zone('body', zones=[
                ui.zone('header'),
                ui.zone('content', zones=[
                    ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                    ui.zone('vertical'),
                    ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
                ]),
            ]),
        ])
    ])])

    # New: side bar names, design and icons
    # New section of help and exit(new #page5)
    q.page['sidebar'] = ui.nav_card(
    box='sidebar',color='primary', title='Conferências', subtitle="Sistema de Gerenciamento",
    value=f'#{q.args["#"]}' if q.args['#'] else '#conferencias-inicio',
    items=[
        ui.nav_group('Menu', items=[
            ui.nav_item(name='#conferencias-inicio',label='Conferências', icon='Globe'),
            ui.nav_item(name='#conferencias-inscricao', label='Inscrições',icon='UserFollowed'),
            ui.nav_item(name='##conferencias-relatorios', label='Relatórios',icon='DietPlanNotebook'),
        ]),
            ui.nav_group('Ajuda', items=[
            ui.nav_item(name='#duvidas', label='Duvidas',icon='Info'),
            ui.nav_item(name='#sair', label='Sair', icon='PowerButton'),
        ]),
    ])

    # New: dropdown in the header section
    q.page['header'] = ui.header_card(
        box='header', title='', subtitle='',
        secondary_items = [ui.dropdown(name='search', label='Search', placeholder='Selecione a conferência...', 
            choices=[
                ui.choice(name='option1', label='Option 1'),
                ui.choice(name='option2', label='Option 2'),
                ui.choice(name='option3', label='Option 3'),
            ],
            width='400px',
            ),
        ],
        items=[
            ui.persona(title='User', subtitle='Developer', size='xs', image='AccountBrowser'),
        ]
    )

    if q.args['#'] is None:
        await page_conferencias_inicio(q)

@app('/')
async def serve(q: Q):
    # Run only once per client connection.
    if not q.client.initialized:
        q.client.initialized = True
        q.client.cards = set()
        await init(q)
        q.client.initialized = True

    # Handle routing.
    await run_on(q)
    await q.page.save()

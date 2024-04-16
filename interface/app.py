from h2o_wave import main, app, Q, ui, on, run_on, data
from typing import Optional, List


# Use for page cards that should be removed when navigating away.
# For pages that should be always present on screen use q.page[key] = ...
def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

# Remove all the cards related to navigation.
def clear_cards(q, ignore: Optional[List[str]] = []) -> None:
    if not q.client.cards:
        return

    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)

@on('#page1') #CHANGED
async def page1(q: Q):
    q.page['sidebar'].value = '#page1'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    # New: top right button added "Nova conferência"
    add_card(q, 'button', ui.form_card(box='horizontal', items = [
        ui.button (name='button', label='Nova Conferência', icon='CirclePlus', primary=True)
    ]))

    # New: Action Section present in the Column (Ação)
    commands = [
        ui.command(name='details', label='Details', icon='Info'),
        ui.command(name='delete', label='Delete', icon='Delete'),
    ]

    # New: Row of conferences listed as placeholders (Nome, Data, Local, Ações) 
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

@on('#page2') #CHANGED
async def page2(q: Q):
    q.page['sidebar'].value = '#page2'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    # New: Conference and Person Register Section
    # Inline to put the elements side to side
    # Values of width and weight are fixed as for now, until i realize how to scale them with the screen   
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


@on('#page3')
async def page3(q: Q):
    q.page['sidebar'].value = '#page3'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    add_card(q, 'form', ui.form_card(box='horizontal', items = [
        ui.text_xl(name='reports', content='Relatórios'),
    ]))

    for i in range(12):
        add_card(q, f'item{i}', ui.wide_info_card(box=ui.box('grid', width='400px'), name='', icon='ReportWarning', title=f'Conferencia {i+1}', caption='Lorem ipsum dolor sit amet'))

@on('#page4')
@on('page4_reset')
async def page4(q: Q):
    q.page['sidebar'].value = '#page4'
    # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    # Since this page is interactive, we want to update its card
    # instead of recreating it every time, so ignore 'form' card on drop.
    clear_cards(q, ['form'])

    # If first time on this page, create the card.
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
async def page4_step2(q: Q):
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
async def page4_step3(q: Q):
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

@on('#page5')
async def page3(q: Q):
    q.page['sidebar'].value = '#page5'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    for i in range(12):
        add_card(q, f'item{i}', ui.wide_info_card(box=ui.box('grid', width='400px'), name='', title='Tile',
                                                  caption='Lorem ipsum dolor sit amet'))

# NEW: default theme, tried a personalized one, but the values seemed off, almost like they were "mixed", so i couldnt find a good balance
async def init(q: Q) -> None: #CHANGED
    q.page['meta'] = ui.meta_card(box='', theme='solarized' ,layouts=[ui.layout( breakpoint='xs', min_height='100vh', zones=[
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
    value=f'#{q.args["#"]}' if q.args['#'] else '#page1',
    items=[
        ui.nav_group('Menu', items=[
            ui.nav_item(name='#page1',label='Conferências', icon='Globe'),
            ui.nav_item(name='#page2', label='Inscrições',icon='UserFollowed'),
            ui.nav_item(name='#page3', label='Relatórios',icon='DietPlanNotebook'),
        ]),
            ui.nav_group('Ajuda', items=[
            ui.nav_item(name='#page4', label='Duvidas',icon='Info'),
            ui.nav_item(name='#page5', label='Sair', icon='PowerButton'),
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
            ui.persona(title='Carol Coelho', subtitle='League of Legends Bronze', size='xs', image='AccountBrowser'),
        ]
    )

    # If no active hash present, render page1.
    if q.args['#'] is None:
        await page1(q)

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

import time
from h2o_wave import main, app, Q, ui, on, run_on 

from conferencias.pages import conferencias_inscricao, conferencias_inicio
from conferencias.pages import ConferenceList
from db_test import create_conferencia


@app("/")
async def serve(q: Q):
    # Run only once per client connection.
    if not q.client.initialized:
        q.client.cards = set()
        q.client.rows = []
        q.client.initialized = True
        await init(q)

#ui.table_row(name='row1', cells=['Conf-Labinfra', '13/12/2024','Castanhal']),

# ------------------------------ INPUT HANDLE ------------------------------ #    
    if q.args.delete_row:
        # Elimina as linhas na tabela
        q.client.rows = [row for row in q.client.rows if row.id != q.args.delete_row]
    if q.args.button_conference_register:
        # Adiciona novas linhas na tabela com nome padrão "New Chat"
        q.client.rows.append(ConferenceList(q.args.conf_name_register_textbox, q.args.conf_date_register_picker, q.args.conf_city_register_textbox))
        conferencia = q.args.conf_name_register_textbox, q.args.conf_date_register_picker, q.args.conf_city_register_textbox
        create_conferencia(conferencia)
        
# ----------------------------------------------------------------------#

    # Forces reload of the screen in conferencias_inicio, conferencias_registro and conferencias_inscricao
    await conferencias_inicio(q)

    # Handles routing
    await run_on(q)
    await q.page.save()


async def start_page(q: Q):
    q.page['sidebar'].value = '#conferencias-inicio'

    q.page['title'] = ui.text(name='', content='')
    q.page['form'] = ui.form_card(box='vertical', items=[
        #ui.button (name='button', label='Nova Conferência', icon='CirclePlus', primary=True, path='#conferencias-registro'),
        ui.link(name='add_conference_button', label='Nova Conferência', path='#conferencias-registro', target='_self', button=True)
    ])

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', theme='lighting', title='Conferências',icon='AddGroup', layouts=[ui.layout( breakpoint='xs', min_height='100vh', zones=[
        ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
            ui.zone('sidebar', size='250px'),
            ui.zone('body', zones=[
                ui.zone('header', direction=ui.ZoneDirection.ROW),
                ui.zone('content', zones=[
                    ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                    ui.zone('vertical'),
                    ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
                ]),
            ]),
            
        ])
    ])])
    
    q.page['sidebar'] = ui.nav_card(box='sidebar',color='primary', title='Conferências', subtitle="Sistema de Gerenciamento",value=f'#{q.args["#"]}' if q.args['#'] else '#conferencias-inicio',
        items=[
            ui.nav_group('Menu', items=[
                ui.nav_item(name='#conferencias-inicio',label='Conferências', icon='Globe'),
                ui.nav_item(name='#conferencias-inscricoes', label='Inscrições',icon='UserFollowed'),
                ui.nav_item(name='#conferencias-relatorios', label='Relatórios',icon='DietPlanNotebook'),
            ]),
                ui.nav_group('Ajuda', items=[
                ui.nav_item(name='#duvidas', label='Duvidas',icon='Info'),
                ui.nav_item(name='#sair', label='Sair', icon='PowerButton'),
            ]),
        ])

    #TROCAR DE CHAT PARA INICIO
    q.page["header"] = ui.header_card(box="header",title="",subtitle="",
        secondary_items=[
            ui.dropdown(name='search',label='Search',placeholder='Selecione a conferência...',
                choices=[
                    ui.choice(name='option1', label='Option 1'),
                    ui.choice(name='option2', label='Option 2'),
                    ui.choice(name='option3', label='Option 3'),
                ],
                width='400px',
            )],
        items=[
            ui.persona(title='User', subtitle='Developer', size='xs', image='AccountBrowser'),
        ],
    )

    if q.args['#'] is None:
        await start_page(q)


    q.page["footer"] = ui.footer_card(
        box="footer",
        caption="Made with [Wave](https://wave.h2o.ai), [h2oGPTe](https://h2o.ai/platform/enterprise-h2ogpte), and "
        "💛 by the Makers at H2O.ai.<br />Find more in the [H2O GenAI App Store](https://genai.h2o.ai/).",
    )

    # If no active hash present, render chat page.
    #if q.args["#"] is None:
        #await chat(q)

def redirect_to_main(q: Q):
    time.sleep(2) 
    q.page['meta'].redirect = '#conferencias-inicio'
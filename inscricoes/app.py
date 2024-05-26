from h2o_wave import main, app, Q, ui, on, run_on

from inscricoes.layout import setup_function

# Utilities
from inscricoes.utilities.handlers import main

@app("/")
async def serve(q: Q):
    # Run only once per client connection.
    if not q.client.initialized:
        q.client.cards = set()
        q.client.rows = []
        await setup_function(q)
        q.client.initialized = True
        await init(q)
    
    # Handles routing
    await run_on(q)
    await q.page.save()

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', theme='lighting', title='Conferências',icon='AddGroup', 
        layouts=[ui.layout(breakpoint='xs', min_height='100vh', 
            zones=[
                ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, 
                    zones=[
                        ui.zone('sidebar', size='250px'),
                        ui.zone('body', 
                            zones=[
                                ui.zone('header', direction=ui.ZoneDirection.ROW),
                                ui.zone('content', 
                                    zones=[
                                        ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                                        ui.zone('vertical'),
                                        ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
                                    ]
                                ),
                            ]
                        ),   
                    ]
                )
            ]
        )]
    )
    
    q.page['sidebar'] = ui.nav_card(box='sidebar',color='primary', title='Conferências', subtitle="Sistema de Gerenciamento",value=f'#{q.args["#"]}' if q.args['#'] else '#conferencias-inicio',
        items=[
            ui.nav_group('Menu', 
                items=[
                    ui.nav_item(name='#conferencias-inicio',label='Conferências', icon='Globe'),
                    ui.nav_item(name='#conferencias-inscricoes', label='Inscrições',icon='UserFollowed'),
                    ui.nav_item(name='#conferencias-relatorios', label='Relatórios',icon='DietPlanNotebook'),
                ]
            ),
            ui.nav_group('Ajuda', 
                items=[
                    ui.nav_item(name='#duvidas', label='Duvidas',icon='Info'),
                    ui.nav_item(name='#sair', label='Sair', icon='PowerButton'),
                ]
            ),
        ]
    )

    #TROCAR DE CHAT PARA INICIO
    q.page["header"] = ui.header_card(box="header",title="",subtitle="",
        items=[
            ui.persona(title='User', subtitle='Developer', size='xs', image='AccountBrowser'),
        ],
    )
    
    if q.args['#'] is None:
        await setup_function(q)
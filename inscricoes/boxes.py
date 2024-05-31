from datetime import datetime
from h2o_wave import main, app, Q, ui, on, run_on 

# Database
from inscricoes.data.db.crud import read_single_conference

# Section to show to the user the LightBox for editing conference.
def box_conference_edit(q: Q, id_row):
    detalhes_conferencia = read_single_conference(id_row)
    detalhes_conferencia_data = datetime.strptime(detalhes_conferencia.data, '%d/%m/%Y').strftime('%Y-%m-%d')
 
    q.page['meta'].dialog = ui.dialog(title='Edite as informações da Conferência', blocking=True, items=[
            ui.text_xl(name='box_conference_edit_title', content='Nova Conferência'),
            ui.textbox(name='box_conference_edit_name', label='Nome', value=detalhes_conferencia.nome),
            ui.date_picker(name='box_conference_edit_date', label='Data', value=detalhes_conferencia_data),
            ui.textbox(name='box_conference_edit_city', label='Local', value=detalhes_conferencia.local),
            ui.text_xl(name='box_space_text', content=''),
            ui.inline(justify='center', items=[
                ui.button(name='box_conference_edit_button_submit', label='Atualizar', primary=True),                          
                ui.button(name='box_exit', label='Cancelar',)
                ]
            )
        ]
    )
 
# Section to show to the user the LightBox for adding new participants.    
def box_participant_add(q: Q):
    q.page['meta'].dialog = ui.dialog(name='create_participant_box',title='Edite as informações da Conferência', blocking=True, items=[
        ui.textbox(name='participant_add_name', label='Nome'),
        ui.textbox(name='participant_add_age', label='Idade'),
        ui.dropdown(name='participant_add_gender', label='Gênero', placeholder='Selecione', 
            choices=[
                ui.choice(name='Masculino', label='Masculino'),
                ui.choice(name='Feminino', label='Feminino'),
            ]
        ),
        ui.dropdown(name='participant_add_pay_type', label='Tipo de Inscrição', placeholder='Completo', 
            choices=[
                ui.choice(name='Completo', label='Completo'),
                ui.choice(name='Isento', label='Isento'),
            ]
        ),
        ui.textbox(name='participant_add_pay_value', label='Valor', placeholder='0.00'),
        ui.inline(justify='center', 
            items=[
                ui.button(name='participant_add_submit_button', label='Adicionar', primary=True),
                ui.button(name='box_exit', label='Cancelar',)
                ]
            )         
        ]
    )
    
#TODO: handle ESC keyboard event to close the LightBox
def box_participant_edit(q: Q, selected_dict): 
    q.page['meta'].dialog = ui.dialog(title='Edite as informações da Conferência', blocking=True, items=[
        ui.textbox(name='participant_edit_name', label='Nome',value=selected_dict['name']),
        ui.textbox(name='participant_edit_age', label='Idade',value=selected_dict['age']),
        ui.dropdown(name='participant_edit_gender', label='Gênero', value=('Masculino' if selected_dict['gender'] == 'Masculino' else 'Feminino'),
            choices=[
                ui.choice(name='Masculino', label='Masculino'),
                ui.choice(name='Feminino', label='Feminino'),
            ]
        ),
        ui.dropdown(name='participant_edit_pay_type', label='Tipo de Inscrição', value=('Completo' if selected_dict['pay_type'] == 'Completo' else 'Isento'),
            choices=[
                ui.choice(name='Isento', label='Isento'),
                ui.choice(name='Completo', label='Completo'),
            ]
        ),
        ui.textbox(name='participant_edit_pay_value', label='Valor', value=selected_dict['pay_value']),
        ui.inline(justify='center', 
            items=[
                ui.button(name='participant_edit_button_submit', label='Atualizar', primary=True),
                ui.button(name='box_exit', label='Cancelar')
                ]
            )         
        ],
        events=[]
    )


    
 
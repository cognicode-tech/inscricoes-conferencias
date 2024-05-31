from datetime import datetime
from h2o_wave import main, app, Q, ui, on, run_on, copy_expando


# Layout
from inscricoes.layout import (conferencias_inicio, conferencias_inicio_table,
                               conferencias_inscricao, conferencias_inscricao_table, conferencia_inscricoes_values)

# Boxes
from inscricoes.boxes import (box_conference_edit, 
                              box_participant_add, box_participant_edit)

# Database
from inscricoes.data.db.crud import (create_conferencia, delete_conferencia, update_conferencia, create_participante,
                                     create_inscricao, read_inscricao_id, read_inscricao, read_inscricoes)

# Utilities
from inscricoes.utilities.utils import (utils_verify_invalid_item, utils_participant_list_values_assert,
                                        utils_participant_list_values, utils_participant_list_edit, ParticipantList)

# Settings
from inscricoes.data.logger import logger

# ------------------- GENERAL ------------------- #

@on('box_exit')
async def box_exit(q: Q):
    q.page['meta'].dialog = None

# --------------------- CONFERENCES SECTION ------------------- #

@on('new_conference_button')
async def add_conference_table(q: Q):
    try: 
        conferencia_data = q.args.new_conference_name.capitalize(),\
            datetime.strptime(q.args.new_conference_date, '%Y-%m-%d').strftime('%d/%m/%Y'),\
                q.args.new_conference_city.capitalize()
        
        conferencia_dict = dict(zip(['name', 'date', 'city'], conferencia_data))
        
        if not utils_verify_invalid_item(q, conferencia_data):
            create_conferencia(conferencia_dict)
            
    except TypeError as TypeErr:
        logger.info(f"Error:{TypeErr}")
        
    except AttributeError as AtrErr:
        logger.info(f"Error:{AtrErr}")
    
    await conferencias_inicio(q)

# Deletes a conference row from the database.   
@on('main_conference_delete_table_row')
async def delete_conference_table_row(q: Q):
    delete_conferencia(q.args.main_conference_delete_table_row)
    await conferencias_inicio_table(q)
    
@on('main_conference_edit_table_row')
async def edit_conference_table_row(q: Q):
    copy_expando(q.args, q.client)
    await q.page.save()
    
    _id = q.client.main_conference_edit_table_row
    box_conference_edit(q,_id)

# Submit the changes in conferences to the database.
@on('box_conference_edit_button_submit') 
async def submit_edit_conference(q: Q):
    _id = q.client.main_conference_edit_table_row
    
    conferencia_data = q.args.box_conference_edit_name.capitalize(), \
        datetime.strptime(q.args.box_conference_edit_date, '%Y-%m-%d').strftime('%d/%m/%Y'), \
            q.args.box_conference_edit_city.capitalize()
    
    conferencia_dict = dict(zip(['name', 'date', 'city'], conferencia_data))
    
    # Check if any field is empty or None        
    if not utils_verify_invalid_item(q, conferencia_data):
        update_conferencia(_id, conferencia_dict)
        
    # Closes the LightBox and Refresh the page.
    await box_exit(q)
    await conferencias_inicio_table(q)

# --------------------- PARTICIPANTS SECTION ------------------- #

# Call the Lightbox for adding participants.
@on('participant_add_button')
async def call_create_participant_box(q: Q):
    copy_expando(q.args, q.client)
    await q.page.save()
    
    box_participant_add(q)

@on('participant_add_submit_button')
async def add_participant_to_table(q: Q):
    participante_data = [q.args.participant_add_name, q.args.participant_add_age,
            q.args.participant_add_gender, q.args.participant_add_pay_type, 
                q.args.participant_add_pay_value]
    try: 
        participante_dict = dict(zip(['name', 'age', 'gender', 'pay_type', 'pay_value'], participante_data))
        
        is_participant_valid = utils_participant_list_values_assert(q, participante_dict['pay_value'])
        if is_participant_valid:
            participante_dict['pay_value'] = is_participant_valid[1]
             
            # Verify if there are None or empty values in participante.        
            if not utils_verify_invalid_item(q, participante_data):
                q.client.rows.append(ParticipantList(participante_dict['name'], participante_dict['age'], 
                                                    participante_dict['gender'], participante_dict['pay_type'], 
                                                    participante_dict['pay_value'], True if participante_data[3] == "Isento" else False))

        
        # Refresh the values of payments and participants in the page.
        q.client.register_total_pay = utils_participant_list_values(q)[0]
        q.client.register_total_people = utils_participant_list_values(q)[1]
        await conferencia_inscricoes_values(q)
    
    except Exception as ValErr:
        logger.info(f"Error:{ValErr}")
    
    # Closes the LightBox and Refresh the page.    
    await box_exit(q)  
    await conferencias_inscricao_table(q)

# Delete the participant in the local table removing the selected row.
@on('participant_delete_row')
async def delete_participant_table_row(q: Q):
    q.client.rows = [row for row in q.client.rows if row.id != q.args.participant_delete_row]
    logger.info(f"Participant {q.args.participant_delete_row} deleted")
    
    # Refresh the values of payments and participants in the page.
    q.client.register_total_pay = utils_participant_list_values(q)[0]
    q.client.register_total_people = utils_participant_list_values(q)[1]
    await conferencia_inscricoes_values(q)
    
    await conferencias_inscricao_table(q)

@on('participant_edit_row')
async def edit_participant_table_row(q: Q):
    copy_expando(q.args, q.client)
    await q.page.save()
    
    _id = q.client.participant_edit_row
      
    # Calls the function to get the selected list.
    selected_list = utils_participant_list_edit(q, _id)

    participant_dict = dict(zip(['id','name', 'age', 'gender', 'pay_type', 'pay_value', 'isento'], selected_list[1]))
    
    # Call the function to show the LightBox for editing participants with pre-filled values by the list.
    box_participant_edit(q, participant_dict)

@on('participant_edit_button_submit')
async def edit_participant_values(q: Q):
   
    # Get the selected row of participants.
    _id = q.client.participant_edit_row
    selected_list = utils_participant_list_edit(q, _id)

    # Create a tuple with the new values.
    participante_data = [q.args.participant_edit_name, q.args.participant_edit_age,
        q.args.participant_edit_gender, q.args.participant_edit_pay_type, 
            q.args.participant_edit_pay_value]
        
    # Verify if there are None, empty or invalid values in participante edit list.
    is_values_valid = utils_participant_list_values_assert(q, participante_data[4])
    
    if is_values_valid:
        participante_data[4] = is_values_valid[1]
        
        participante_dict = dict(zip(['name', 'age', 'gender', 'pay_type', 'pay_value', 'isento'], participante_data))

        # Prevents exceptions from None or empty values.
        if not utils_verify_invalid_item(q, participante_data):
            
            # Change the label of the gender and pay type.        
            q.client.rows[selected_list[0]] = ParticipantList(participante_dict['name'], participante_dict['age'], 
                                                    participante_dict['gender'], participante_dict['pay_type'], 
                                                    participante_dict['pay_value'], True if participante_data[3] == "Isento" else False)
            
        logger.info(f"Participant {q.client.participant_edit_row} edited")
    
    # Refresh the values of payments and participants in the page.
    q.client.register_total_pay = utils_participant_list_values(q)[0]
    q.client.register_total_people = utils_participant_list_values(q)[1]
    await conferencia_inscricoes_values(q)
    
    # Closes the LightBox and Refresh the page.
    await box_exit(q)       
    await conferencias_inscricao_table(q)

@on('submit_conference_registration_button')
async def submit_conference_registration(q: Q):
    participant_list = []
    participante_dict = {}
    copy_expando(q.args, q.client)
    
    #TODO Change this behaviour.
    try:
        total_conference_data = [int(q.client.register_select_conference),q.client.register_responsable,q.client.register_city,q.client.register_estate,\
            q.client.register_pay_paper, q.client.register_pay_deposit, q.client.register_pay_transfer, q.client.register_pay_check]
    
        #TODO - Fix the behaviour of this function (it's changed to always return False at this moment)
        if not utils_verify_invalid_item(q, total_conference_data[0:3]):
            participantes = q.client.rows     
            lista_participantes = [list(value for value in vars(participant).values()) for participant in participantes]
            for _, participante in enumerate(lista_participantes):
                participant_list.append(participante)
                # Key value to reference each participant in the dictionary.
                key = participante[0]
                # Values from each participant.
                values = participante[1:]
                participante_dict[key] = dict(zip(['name', 'age', 'gender', 'pay_type', 'pay_value', 'isento'], values))
                
            # Append the observations (Optional) and the list of participants.    
            total_conference_data.append(q.client.register_observations)
            
            total_conference_dict = dict(zip(['conference_id','responsable','city','estate','pay_paper','pay_deposit','pay_transfer','pay_check','observations'], total_conference_data))
            
            total_conference_dict['total_pay'] = q.client.register_total_pay
            #total_conference_dict['total_persons'] = q.client.register_total_people
            
            #TODO: NEXT VALUES FROM PAYMENTS
            create_inscricao(total_conference_dict)
            
            # TODO - Temporary Solution - this will read the last generated id inscricao id, can lead to some problems.
            _inscricao_id = read_inscricao_id()
            
            # Create the participants.
            for participant_id, participant_values in participante_dict.items():
                participant_values['inscricao_id'] = _inscricao_id
                create_participante(participant_values)
    except Exception as Err:
        logger.info(f"Error:{Err}")
        
    await q.page.save()
    await conferencias_inscricao(q)
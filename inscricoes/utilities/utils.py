from h2o_wave import main, app, Q, ui, on, run_on
from typing import Optional, List

from inscricoes.data.logger import logger
from inscricoes.data.db.crud import read_multiple_conferences, read_single_conference

# Add a card to the page.
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

# Check if any field is empty or None
def utils_verify_invalid_item(q: Q, item):
    return any(value is None or value == '' for value in item)

# Verify if there are None, empty or invalid values in participante list and format (,) to (.), prevents exceptions from float conversion.
def utils_participant_list_values_assert(q: Q, participante_pay):
    try:
        if (participante_pay.count('.') == 1 and participante_pay.count(',') == 0) or (participante_pay.count('.') == 0 and participante_pay.count(',') == 1):
            if all(c in '0123456789.,' for c in participante_pay):
                if ',' in participante_pay:
                    participante_pay = '{:.2f}'.format(float(participante_pay.replace(',', '.')))
                elif '.' in participante_pay:
                    participante_pay = '{:.2f}'.format(float(participante_pay))
                return [True, participante_pay]
        elif (all(c in '0123456789' for c in participante_pay)):
            return [True, participante_pay]
        else:
            return False
    except AttributeError:
        return False
    except Exception as Err:
        logger.info(f"Error:{Err}") 

# Get the total payment value and number of participants   
def utils_participant_list_values(q: Q):
    pagamento_total = 0
    cont = 0
    participantes = q.client.participant_list    
    lista_participantes = [list(value for value in vars(participant).values()) for participant in participantes]
    for _, participante in enumerate(lista_participantes):
        if participante[4] == "Completo":
            pagamento_total += float(participante[5])
        cont+=1
    return [str(pagamento_total), str(cont)]

# Unpack and get the selected Index and row from the table
def utils_participant_list_edit(q: Q, id_row):
    # Unpack and get the selected row from the table
    lista_participantes = [list(value for value in vars(participant).values()) for participant in q.client.participant_list]
    index = next((i for i, sublist in enumerate(lista_participantes) if sublist[0] == id_row), None)
    for _, participante in enumerate(lista_participantes):
        if participante[0] == id_row:
            selected_list = participante
            break
    return [index, selected_list]


# Class to manage the list of participants                
class ParticipantList:
    _id = 0

    def __init__(self, name, age, gender, type_register, value, free_pay):
        ParticipantList._id += 1
        self.id = f'{ParticipantList._id}'
        self.name = name
        self.age = age
        self.gender = gender
        self.type_register = type_register
        self.value = value
        self.free_pay = free_pay
        

def utils_get_single_conference(id_row):
    conference = read_single_conference(id_row)
    return conference
    
def utils_get_multiple_conferences():
    conferences=read_multiple_conferences()
    return conferences

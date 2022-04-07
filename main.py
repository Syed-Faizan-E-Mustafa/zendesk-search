"""
main file to execute the script
"""
import json
import sys


def check_to_quit(user_input):
    """
    exits the program if user enters 'quit'
    Params:
        user_input <string>: user input from the command line interface
    """
    if user_input.lower() == 'quit':
        sys.exit()


def load_data(json_dump_path):
    """
    loads json file as a list of dict objects

    Params:
        json_dump_path <string>: path to the json dump that has to be loaded

    Returns:
        list: list of dict objects
    """
    with open(json_dump_path, encoding='UTF-8') as json_dump:
        return json.load(json_dump)


def show_message(message, line_spacing=0, user_input=False):
    """
    prints the given string on screen and adds specified line spacing

    Params:
        message <string>: message to display on screen
        line_spacing <int>: number of lines to leave blank after the message
        user_input <bool>: determines whether user input is required or not
    """
    line_break = '\n' * line_spacing
    if user_input:
        return input(f'{message}{line_break}')
    print(f'{message}{line_break}')
    return None


def welcome_block():
    """
    prints welcome message and general instructions on screen and waits for user input
    """
    show_message(message='Welcome to Zendesk Search')
    user_input = show_message(
        message="Type 'quit' to exit at any time, Press 'Enter' to continue",
        line_spacing=2,
        user_input=True
    )
    check_to_quit(user_input)


def search_options_block():
    """
    prints search options on screen and waits for user input

    Returns:
         user_input <string>: user input from the command line interface if it is not 'quit'
    """
    show_message(message='\tSelect search options:')
    show_message(message='\t * Press 1 to search Zendesk')
    show_message(message='\t * Press 2 to view a list of searchable fields')
    user_input = show_message(
        message="\t * Type 'quit' to exit",
        line_spacing=2,
        user_input=True
    )
    check_to_quit(user_input)
    return user_input


def show_results(results):
    """
    prints all attributes of the objects in required tabular form

    Params:
        results: dict objects against user search query
    """
    show_message(message=100 * '_')
    for data in results:
        for attribute in data:
            print(f'{attribute:30} {data[attribute]}')
        show_message(message=100*'_', line_spacing=2)


def dataset_search(dataset, term, value):
    """
    searches for the term, and it's value in the selected dataset

    Params:
        dataset: user selected dataset
        term: user cli input for a term to search against
        value: user cli input for a value to search for
    """
    datasets = {
        '1': 'users',
        '2': 'tickets',
        '3': 'organizations',
    }

    data = load_data(f'data/{datasets[dataset]}.json')

    results = []

    for datum in data:
        try:
            if isinstance(datum[term], list):
                if str(value) in [datum_value.lower() for datum_value in datum[term]]:
                    results.append(datum)
                    continue
            if str(value) == str(datum[term]).lower():
                results.append(datum)
        except KeyError:
            show_message(message='Invalid search term.', line_spacing=2)
            return

    if results:
        show_results(results)
        return
    show_message('Not data found.', line_spacing=2)


def dataset_search_block(user_input):
    """
    asks for user to select a field to search against and a value to search for

    Returns:
        dataset_found <bool>: True if the selected dataset exists else False
    """
    if user_input in ['1', '2', '3']:
        search_term = show_message(message='Enter search term', line_spacing=1, user_input=True)
        check_to_quit(search_term)
        search_value = show_message(message='Enter search value', line_spacing=1, user_input=True)
        check_to_quit(search_value)
        dataset_search(dataset=user_input, term=search_term.lower(), value=search_value.lower())
        return True

    return False


def dataset_options_block():
    """
    prints dataset options on screen and waits for user input
    """
    while True:
        user_input = show_message(
            message='Select 1) Users or 2) Tickets or 3) Organizations',
            line_spacing=1,
            user_input=True
        )
        check_to_quit(user_input)

        if dataset_search_block(user_input):
            break


def searchable_fields_block():
    """
    prints all searchable fields for every available dataset
    """
    users_dataset_fields = load_data('data/users.json')[0].keys()
    tickets_dataset_fields = load_data('data/tickets.json')[0].keys()
    organizations_dataset_fields = load_data('data/organizations.json')[0].keys()

    show_message(100*'_')
    show_message('Search Users with')
    for field in users_dataset_fields:
        print(f'{field}')
    show_message(100 * '_')
    show_message('Search Tickets with')
    for field in tickets_dataset_fields:
        print(f'{field}')
    show_message(100 * '_')
    show_message('Search Organizations with')
    for field in organizations_dataset_fields:
        print(f'{field}')
    show_message(100 * '_', line_spacing=2)


if __name__ == '__main__':
    welcome_block()
    while True:
        search_options_input = search_options_block()
        if search_options_input == '1':
            dataset_options_block()
        elif search_options_input == '2':
            searchable_fields_block()

def main_menu():
    while True:
        print("""
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria\n""")

        user_input = input("Enter an option:")
        if user_input not in ['0', '1', '2']:
            print("Invalid option!\n")
        else:
            if user_input == '0':
                print('Have a nice day!\n')
                break
            elif user_input == '1':
                crud_menu()
            else:
                top_ten_menu()


def crud_menu():
    print("""
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies\n""")

    user_input = input("Enter an option:")
    if user_input not in ['0', '1', '2', '3', '4', '5']:
        print("Invalid option!\n")
    else:
        if user_input == '1':
            create_company()
        elif user_input == '2':
            read_company()
        elif user_input == '3':
            update_company()
        elif user_input == '4':
            delete_company()
        elif user_input == '5':
            list_companies()
        else:  # user asked to go back
            pass


def top_ten_menu():
    print("""
TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA\n""")

    user_input = input("Enter an option:")
    if user_input not in ['0', '1', '2', '3']:
        print("Invalid option!\n")
    else:
        if user_input == '1':
            list_by_nd()
        elif user_input == '2':
            list_by_roa()
        elif user_input == '3':
            list_by_roa()
        else:  # user asked to go back
            pass


# CRUD MENU actions
def create_company():
    print('Not implemented!\n')


def read_company():
    print('Not implemented!\n')


def update_company():
    print('Not implemented!\n')


def delete_company():
    print('Not implemented!\n')


def list_companies():
    print('Not implemented!\n')


# TOP TEN MENU actions
def list_by_nd():
    print('Not implemented!\n')


def list_by_roe():
    print('Not implemented!\n')


def list_by_roa():
    print('Not implemented!\n')


if __name__ == '__main__':
    main_menu()

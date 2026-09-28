from views import MenuClientes, ClienteController


def main():
    menu = MenuClientes(ClienteController)
    menu.ejecutar()


if __name__ == "__main__":
    main()
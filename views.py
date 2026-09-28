from models import Cliente


class ClienteController:
    _clientes = []          # lista compartida (atributo de clase)
    _next_id  = 1           # autoincremental

    # ---------- CRUD básico ----------
    @classmethod
    def listar(cls):
        return cls._clientes

    @classmethod
    def agregar(cls, cliente):
        cls._clientes.append(cliente)
        return cliente

    @classmethod
    def buscar_por_id(cls, id_cliente):
        for c in cls._clientes:
            if c.id_cliente == id_cliente:
                return c
        return None

    @classmethod
    def buscar_por_nombre(cls, texto):
        texto = texto.lower()
        return [c for c in cls._clientes
                if texto in c.nombre_completo.lower()]

    @classmethod
    def actualizar(cls, id_cliente, **campos):
        cliente = cls.buscar_por_id(id_cliente)
        if cliente is None:
            raise ValueError(f"No existe cliente con id {id_cliente}")

        for campo, valor in campos.items():
            if campo == "telefono":
                cliente.telefono = valor          # pasa por el setter
            elif campo == "nombre":
                cliente._Cliente__nombre = valor  # o un setter dedicado
            elif campo == "apellido":
                cliente._Cliente__apellido = valor
            else:
                setattr(cliente, campo, valor)
        return cliente

    @classmethod
    def eliminar(cls, id_cliente):
        cliente = cls.buscar_por_id(id_cliente)
        if cliente is None:
            return False
        cls._clientes.remove(cliente)
        return True

    # ---------- Creador de ID ----------
    @classmethod
    def nuevo_id(cls):
        id_actual = cls._next_id
        cls._next_id += 1
        return id_actual

    # ---------- Reportes / agrupaciones ----------
    @classmethod
    def agrupar_por_ciudad(cls):
        agrupados = {}
        for objeto in cls.listar():
            ciudad = objeto.ciudad or "Sin ciudad"
            agrupados.setdefault(ciudad, []).append(objeto.nombre_completo)
        return agrupados

    @classmethod
    def resumen(cls):
        return f"Total de clientes: {len(cls._clientes)}"


def imprimir_titulo(texto):
    print("\n" + "=" * 40)
    print(f"  {texto}")
    print("=" * 40)


class MenuClientes:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.opciones = {
            "1": ("Listar clientes",        self.listar),
            "2": ("Agregar cliente",        self.agregar),
            "3": ("Buscar cliente",         self.buscar),
            "4": ("Actualizar cliente",     self.actualizar),
            "5": ("Eliminar cliente",       self.eliminar),
            "6": ("Ver resumen",            self.resumen),
            "7": ("Cargar desde texto",     self.cargar_texto),
            "8": ("Clientes por ciudad",    self.por_ciudad),
            "0": ("Salir",                  self.salir),
        }

    # ---------- Bucle principal ----------
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Opción: ").strip()
            accion = self.opciones.get(opcion)
            if accion is None:
                print("⚠️ Opción inválida")
                continue
            _, metodo = accion
            if metodo() is False:      # convención: False = salir
                break

    def mostrar_menu(self):
        imprimir_titulo("MENÚ CLIENTES")
        for clave, (descripcion, _) in self.opciones.items():
            print(f"  {clave}. {descripcion}")

    def pausa(self):
        input("\nEnter para continuar...")

    def salir(self):
        print("👋 Hasta luego")
        return False

    # ---------- Acciones del menú ----------
    def listar(self):
        imprimir_titulo("LISTA DE CLIENTES")
        clientes = self.__controlador.listar()
        if not clientes:
            print("  (sin clientes registrados)")
        else:
            for c in clientes:
                print(f"  {c}")
        self.pausa()

    def agregar(self):
        imprimir_titulo("AGREGAR CLIENTE")
        try:
            nombre   = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email    = input("Email: ").strip()
            telefono = input("Teléfono (10 dígitos o vacío): ").strip()
            ciudad   = input("Ciudad: ").strip()

            nuevo = Cliente(
                ClienteController.nuevo_id(),
                nombre, apellido, email, telefono, ciudad,
            )
            self.__controlador.agregar(nuevo)
            print(f"✅ Cliente agregado: {nuevo.nombre_completo}")
        except ValueError as e:
            print(f"❌ Error: {e}")
        self.pausa()

    def buscar(self):
        imprimir_titulo("BUSCAR CLIENTE")
        texto = input("Nombre a buscar: ").strip()
        resultados = self.__controlador.buscar_por_nombre(texto)
        if not resultados:
            print("  (sin resultados)")
        else:
            for c in resultados:
                print(f"  {c}")
        self.pausa()

    def actualizar(self):
        imprimir_titulo("ACTUALIZAR CLIENTE")
        try:
            id_cliente = int(input("ID del cliente: "))
        except ValueError:
            print("❌ ID inválido")
            return self.pausa()

        cliente = self.__controlador.buscar_por_id(id_cliente)
        if cliente is None:
            print("❌ No existe ese cliente")
            return self.pausa()

        print(f"Cliente actual: {cliente}")
        print("(deja en blanco los campos que no quieras cambiar)")

        cambios = {}
        for campo in ("nombre", "apellido", "email", "telefono", "ciudad"):
            nuevo = input(f"  {campo} [{getattr(cliente, campo, '')}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

        if not cambios:
            print("Sin cambios")
        else:
            try:
                self.__controlador.actualizar(id_cliente, **cambios)
                print("✅ Cliente actualizado")
            except ValueError as e:
                print(f"❌ Error: {e}")
        self.pausa()

    def eliminar(self):
        imprimir_titulo("ELIMINAR CLIENTE")
        try:
            id_cliente = int(input("ID a eliminar: "))
        except ValueError:
            print("❌ ID inválido")
            return self.pausa()

        if self.__controlador.eliminar(id_cliente):
            print("✅ Cliente eliminado")
        else:
            print("❌ No se encontró el cliente")
        self.pausa()

    def resumen(self):
        imprimir_titulo("RESUMEN")
        print(f"  {self.__controlador.resumen()}")
        print(f"  {Cliente.total_creados} clientes creados en total (histórico)")
        self.pausa()

    def cargar_texto(self):
        imprimir_titulo("CARGAR DESDE TEXTO")
        linea = input('Formato: "1, Ana, Pérez, ana@x.com"\n> ')
        try:
            cliente = Cliente.desde_texto(linea)
            self.__controlador.agregar(cliente)
            print(f"✅ Cargado: {cliente}")
        except (ValueError, IndexError) as e:
            print(f"❌ Error: {e}")
        self.pausa()

    def por_ciudad(self):
        imprimir_titulo("CLIENTES POR CIUDAD")
        agrupados = self.__controlador.agrupar_por_ciudad()
        if not agrupados:
            print("  (sin clientes)")
        else:
            for ciudad, nombres in agrupados.items():
                print(f"  {ciudad}: {', '.join(nombres)}")
        self.pausa()
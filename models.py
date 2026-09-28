class Cliente:
    total_creados = 0   # atributo de CLASE

    def __init__(self, id_cliente, nombre, apellido, email,
                 telefono="", ciudad=None):
        self.id_cliente = id_cliente
        self.__nombre = nombre
        self.__apellido = apellido
        self.email = email
        self.telefono = telefono          # usa el setter
        self.ciudad = ciudad
        Cliente.total_creados += 1

    # ---------- Propiedades calculadas ----------
    @property
    def iniciales(self):
        return f"{self.__nombre[0]}.{self.__apellido[0]}.".upper()

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    # ---------- Validación de teléfono ----------
    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    @staticmethod
    def es_telefono_valido(texto):
        texto = str(texto).strip()
        return texto == "" or (texto.isdigit() and len(texto) == 10)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = Cliente.limpiar(valor)
        if not Cliente.es_telefono_valido(valor):
            raise ValueError("El teléfono debe tener 10 dígitos")
        self.__telefono = valor

    # ---------- Fábrica desde texto ----------
    @classmethod
    def desde_texto(cls, linea):
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) < 4:
            raise ValueError("Se esperaban al menos 4 datos separados por comas")
        id_cliente, nombre, apellido, email = partes[:4]
        return cls(int(id_cliente), nombre, apellido, email)

    # ---------- Representación ----------
    def __repr__(self):
        return f"Cliente(id={self.id_cliente}, {self.nombre_completo})"

    def __str__(self):
        return (f"[{self.id_cliente}] {self.nombre_completo} "
                f"| {self.email} | {self.telefono or 'sin teléfono'} "
                f"| {self.ciudad or 'sin ciudad'}")
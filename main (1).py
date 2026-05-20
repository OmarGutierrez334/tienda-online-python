from datetime import datetime


class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock


class SistemaCompras:
    def __init__(self):
        self.usuario_actual = ""
        self.carrito = []


        self.productos = [
            Producto("Portatil", 2000000, 5),
            Producto("Mouse", 150000, 20),
            Producto("Teclado", 100000, 10),
            Producto("Monitor", 800000, 8),
            Producto("Audifonos", 250000, 15)
        ]

   
    def formatear(self, precio):
        return "$" + "{:,}".format(precio).replace(",", ".")

    def linea(self):
        print("=" * 50)

   
    def registrar(self):
        self.linea()
        print("REGISTRO DE USUARIO")
        self.linea()

     
        while True:
            usuario = input("Nuevo usuario: ").strip()

            if usuario == "":
                print("El usuario no puede estar vacío ni contener solo espacios.")
            else:
                break

    
        while True:
            contraseña = input("Nueva contraseña: ").strip()

            if contraseña == "":
                print("La contraseña no puede estar vacía ni contener solo espacios.")
            else:
                break

     
        try:
            with open("usuarios.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    if usuario == datos[0]:
                        print("Ese usuario ya existe.")
                        return
        except FileNotFoundError:
            pass

      
        with open("usuarios.txt", "a", encoding="utf-8") as archivo:
            archivo.write(usuario + "," + contraseña + "\n")

        print("Usuario registrado correctamente.")


    def login(self):
        self.linea()
        print("INICIO DE SESIÓN")
        self.linea()

        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()

        try:
            with open("usuarios.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    if usuario == datos[0] and contraseña == datos[1]:
                        self.usuario_actual = usuario
                        print("Login correcto.")
                        return True
        except FileNotFoundError:
            print("No hay usuarios registrados.")
            return False

        print("Datos incorrectos.")
        return False


    def cargar_carrito(self):
        self.carrito = []

        try:
            with open(
                "carrito_" + self.usuario_actual + ".txt",
                "r",
                encoding="utf-8"
            ) as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    self.carrito.append((datos[0], int(datos[1])))
        except FileNotFoundError:
            pass

    def guardar_carrito(self):
        with open(
            "carrito_" + self.usuario_actual + ".txt",
            "w",
            encoding="utf-8"
        ) as archivo:
            for producto in self.carrito:
                archivo.write(
                    producto[0] + "," + str(producto[1]) + "\n"
                )

   
    def mostrar_productos(self):
        self.linea()
        print("LISTA DE PRODUCTOS")
        self.linea()

        for i in range(len(self.productos)):
            producto = self.productos[i]
            print(
                f"{i + 1}. {producto.nombre:<12} - "
                f"{self.formatear(producto.precio):<12} "
                f"| Stock: {producto.stock}"
            )

        self.linea()

    
    def comprar(self):
        self.mostrar_productos()

        try:
            opcion = int(input("Elige el número del producto: "))

            if opcion < 1 or opcion > len(self.productos):
                print("Opción inválida.")
                return

            producto = self.productos[opcion - 1]

            if producto.stock <= 0:
                print("No hay stock disponible.")
                return

          
            self.carrito.append((producto.nombre, producto.precio))

        
            producto.stock -= 1

         
            self.guardar_carrito()

            print(f"{producto.nombre} agregado al carrito.")

        except ValueError:
            print("Entrada inválida.")

  
    def ver_carrito(self):
        self.linea()
        print("CARRITO DE COMPRAS")
        self.linea()

        total = 0

        if len(self.carrito) == 0:
            print("Carrito vacío.")
        else:
            for i in range(len(self.carrito)):
                producto = self.carrito[i]
                print(
                    f"{i + 1}. {producto[0]:<12} - "
                    f"{self.formatear(producto[1])}"
                )
                total += producto[1]

            print("-" * 50)
            print(f"TOTAL: {self.formatear(total)}")

        self.linea()


    def eliminar_del_carrito(self):
        if len(self.carrito) == 0:
            print("El carrito está vacío.")
            return

        self.ver_carrito()

        try:
            opcion = int(
                input("Ingrese el número del producto que desea eliminar: ")
            )

            if opcion < 1 or opcion > len(self.carrito):
                print("Opción inválida.")
                return

            producto_eliminado = self.carrito.pop(opcion - 1)

        
            for producto in self.productos:
                if producto.nombre == producto_eliminado[0]:
                    producto.stock += 1
                    break

            self.guardar_carrito()

            print(f"{producto_eliminado[0]} eliminado del carrito.")

        except ValueError:
            print("Entrada inválida.")


    def vaciar_carrito(self):
        if len(self.carrito) == 0:
            print("El carrito ya está vacío.")
            return

        for item in self.carrito:
            for producto in self.productos:
                if producto.nombre == item[0]:
                    producto.stock += 1
                    break

        self.carrito = []
        self.guardar_carrito()

        print("Carrito vaciado correctamente.")


    def finalizar_compra(self):
        if len(self.carrito) == 0:
            print("El carrito está vacío.")
            return

        self.ver_carrito()

        self.linea()
        print("MÉTODOS DE PAGO")
        self.linea()
        print("1. Tarjeta de crédito")
        print("2. Nequi")
        print("3. Daviplata")
        print("4. PSE")
        print("5. Contra entrega")
        self.linea()

        opcion = input("Seleccione un método de pago: ")

        metodos = {
            "1": "Tarjeta de crédito",
            "2": "Nequi",
            "3": "Daviplata",
            "4": "PSE",
            "5": "Contra entrega"
        }

        if opcion not in metodos:
            print("Método de pago inválido.")
            return

        metodo_pago = metodos[opcion]
        total = sum(producto[1] for producto in self.carrito)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    
        self.linea()
        print("FACTURA DE COMPRA")
        self.linea()
        print(f"Cliente: {self.usuario_actual}")
        print(f"Fecha: {fecha}")
        print(f"Método de pago: {metodo_pago}")
        print("-" * 50)

        for producto in self.carrito:
            print(
                f"{producto[0]:<12} - "
                f"{self.formatear(producto[1])}"
            )

        print("-" * 50)
        print(f"TOTAL PAGADO: {self.formatear(total)}")
        self.linea()

       
        with open(
            "historial_" + self.usuario_actual + ".txt",
            "a",
            encoding="utf-8"
        ) as archivo:
            archivo.write(
                f"\nFecha: {fecha}\n"
                f"Método de pago: {metodo_pago}\n"
            )

            for producto in self.carrito:
                archivo.write(
                    f"{producto[0]} - {self.formatear(producto[1])}\n"
                )

            archivo.write(
                f"TOTAL: {self.formatear(total)}\n"
                + "=" * 50
                + "\n"
            )

      
        self.carrito = []
        self.guardar_carrito()

        print("Compra realizada con éxito.")


    def ver_historial(self):
        self.linea()
        print("HISTORIAL DE COMPRAS")
        self.linea()

        try:
            with open(
                "historial_" + self.usuario_actual + ".txt",
                "r",
                encoding="utf-8"
            ) as archivo:
                contenido = archivo.read()

                if contenido.strip() == "":
                    print("No hay compras registradas.")
                else:
                    print(contenido)

        except FileNotFoundError:
            print("No hay compras registradas.")

        self.linea()


    def menu(self):
        while True:
            self.linea()
            print("SISTEMA DE COMPRAS ONLINE")
            self.linea()
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            self.linea()

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                if self.login():
                    self.cargar_carrito()

                    while True:
                        self.linea()
                        print(f"MENÚ DE {self.usuario_actual.upper()}")
                        self.linea()
                        print("1. Ver productos")
                        print("2. Comprar producto")
                        print("3. Ver carrito")
                        print("4. Eliminar producto del carrito")
                        print("5. Vaciar carrito")
                        print("6. Finalizar compra")
                        print("7. Ver historial de compras")
                        print("8. Cerrar sesión")
                        self.linea()

                        opcion_usuario = input("Elige una opción: ")

                        if opcion_usuario == "1":
                            self.mostrar_productos()
                        elif opcion_usuario == "2":
                            self.comprar()
                        elif opcion_usuario == "3":
                            self.ver_carrito()
                        elif opcion_usuario == "4":
                            self.eliminar_del_carrito()
                        elif opcion_usuario == "5":
                            self.vaciar_carrito()
                        elif opcion_usuario == "6":
                            self.finalizar_compra()
                        elif opcion_usuario == "7":
                            self.ver_historial()
                        elif opcion_usuario == "8":
                            print("Sesión cerrada.")
                            self.usuario_actual = ""
                            self.carrito = []
                            break
                        else:
                            print("Opción inválida.")

            elif opcion == "2":
                self.registrar()

            elif opcion == "3":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida.")


if __name__ == "__main__":
    sistema = SistemaCompras()
    sistema.menu()
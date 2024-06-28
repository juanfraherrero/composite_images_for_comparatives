import tkinter as tk
from tkinter import filedialog, messagebox

from uiBackend import generateComposite


class CompositeImagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Composite images")

        # Configurar la fuente global
        default_font = ("Helvetica", 12)
        self.root.option_add("*Font", default_font)

        # Botón para elegir la ubicación y el nombre del archivo resultante
        tk.Label(root, text="Output:").grid(row=0, column=0, sticky="we")
        self.output_entry = tk.Entry(root)
        self.output_entry.grid(row=0, column=1, columnspan=3, sticky="we")
        self.browse_output_button = tk.Button(
            root, text="Browse", command=self.browse_output
        )
        self.browse_output_button.grid(row=0, column=4, sticky="w")

        tk.Label(root, text="Size:").grid(row=1, column=0, sticky="we")
        self.size = tk.Entry(root)
        self.size.grid(row=1, column=1, columnspan=3, sticky="we")

        # Cantidad de columnas
        tk.Label(root, text="Quantity of columns:").grid(row=2, column=0, sticky="we")
        self.columns_entry = tk.Entry(root)
        self.columns_entry.grid(row=2, column=1, columnspan=3, sticky="we")

        # Botón para generar campos de archivo
        self.generate_button = tk.Button(
            root, text="Generate Columns", command=self.generate_file_fields
        )
        self.generate_button.grid(row=3, column=0, columnspan=5, sticky="nswe")

        # Contenedor para los campos de archivo
        self.files_frame = tk.Frame(root)
        self.files_frame.grid(row=4, column=0, columnspan=5, sticky="nswe")

        # Botón para crear el arreglo de imágenes
        self.create_button = tk.Button(
            root, text="Create Composite", command=self.create_composite
        )
        self.create_button.grid(row=5, column=0, columnspan=5, sticky="nswe")

        self.file_entries = []
        self.column_name_entries = []

        # Configurar la cuadrícula para redimensionar
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.columnconfigure(5, weight=1)
        # self.root.rowconfigure(4, weight=1)
        self.files_frame.columnconfigure(0, weight=1)
        self.files_frame.columnconfigure(1, weight=1)
        self.files_frame.columnconfigure(2, weight=1)
        self.files_frame.columnconfigure(3, weight=1)

    def browse_output(self):
        output_file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")],
        )
        if output_file:
            self.output_entry.delete(
                0, tk.END
            )  # Limpiar la entrada antes de insertar el nuevo archivo
            self.output_entry.insert(0, output_file)

    def generate_file_fields(self):
        # Limpiar campos anteriores
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        self.file_entries.clear()
        self.column_name_entries.clear()

        try:
            columns = int(self.columns_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor, ingresa un número válido de columnas."
            )
            return

        for i in range(columns):
            tk.Label(self.files_frame, text="Name:").grid(row=i, column=0, sticky="we")
            column_name_entry = tk.Entry(self.files_frame)
            column_name_entry.grid(row=i, column=1, sticky="we")
            self.column_name_entries.append(column_name_entry)

            tk.Label(self.files_frame, text="Files:").grid(row=i, column=2, sticky="we")
            entry = tk.Entry(self.files_frame)
            entry.grid(row=i, column=3, sticky="we")
            browse_button = tk.Button(
                self.files_frame,
                text="Browse",
                command=lambda e=entry: self.browse_files(e),
            )
            browse_button.grid(row=i, column=4, sticky="w")
            self.file_entries.append(entry)

    def browse_files(self, entry):
        files = filedialog.askopenfilenames(
            filetypes=[("Image files", ["*.png", "*.jpg", "*.jpeg"])]
        )
        entry.delete(0, tk.END)  # Limpiar la entrada antes de insertar nuevos archivos
        entry.insert(0, ", ".join(files))

    def create_composite(self):
        output = self.output_entry.get()
        if not output:
            messagebox.showerror("Error", "Please, enter a valid output file name.")
            return

        try:
            size = int(self.size.get())
        except ValueError:
            messagebox.showerror("Error", "Please, enter a valid size.")
            return

        images_paths = []
        for entry in self.file_entries:
            files = entry.get().split(", ")
            if files:
                images_paths.append(files)

        column_names = [entry.get() for entry in self.column_name_entries]

        generateComposite(images_paths, size, column_names, output)
        print("Resultado:", output)
        print("Arreglo de imágenes seleccionadas:", images_paths)
        print("Tamaño de las imágenes:", size)
        print("Nombres de las columnas:", column_names)
        # Aquí puedes llamar a tu función para procesar las imágenes


if __name__ == "__main__":
    root = tk.Tk()
    app = CompositeImagesApp(root)
    root.mainloop()

from PIL import Image, ImageDraw, ImageFont


def generateComposite(images, size, column_names, output) -> None:

    # Función para recortar la imagen desde centro
    def crop_center(image, crop_size):
        width, height = image.size
        new_width, new_height = crop_size
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        return image.crop((left, top, right, bottom))

    images = [
        [
            crop_center(Image.open(image_path), (size, size))
            for image_path in image_paths
        ]
        for image_paths in images
    ]

    # Asumimos que todas las imágenes tienen el mismo tamaño
    width, height = size, size

    cant_columns = len(images)
    cant_rows = len(
        max(images, key=len)
    )  # obtener la mayopr cantidad de imagenes en una columnas

    spacing = 10  # Definir espacio entre imágenes
    col_name_height = 64  # Definir altura de los nombres de las columnas

    total_width = (width + spacing) * cant_columns + spacing
    total_height = (height + spacing) * cant_rows + spacing + col_name_height

    # Crear una nueva imagen con el tamaño adecuado
    new_image = Image.new("RGB", (total_width, total_height), color="white")

    # Crear objeto de dibujo
    draw = ImageDraw.Draw(new_image)

    # Definir la fuente para los nombres de las columnas
    try:
        font = ImageFont.truetype("arial.ttf", col_name_height)
        print("Font loaded successfully")
    except IOError:
        font = ImageFont.load_default()

    # Dibujar los nombres de las columnas
    for index, column in enumerate(column_names):
        draw.text(
            (
                (width + spacing) * (index)
                + (width // 2)
                - draw.textsize(column, font=font)[0] // cant_columns,
                0,
            ),
            column,
            fill="black",
            font=font,
        )

    # Pegar las imágenes en la nueva imagen
    for i in range(cant_rows):
        for j in range(cant_columns):
            if images[j][i] is not None:  # Si hay una imagen en esa posición
                new_image.paste(
                    images[j][i],
                    (
                        j * (width + spacing) + spacing,
                        col_name_height + spacing + i * (height + spacing),
                    ),
                )

    # Guardar la nueva imagen
    new_image.save(output)

    # Mostrar la nueva imagen (opcional)
    new_image.show()

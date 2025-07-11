import ipywidgets as widgets


def get_upload_widget() -> widgets.FileUpload:

    upload = widgets.FileUpload(
        accept=".csv",
        multiple=False,
        description="📁 Selecionar CSV",
        style={"font_weight": "bold"},
        layout=widgets.Layout(padding="8px 15px", width="auto"),
    )
    return upload

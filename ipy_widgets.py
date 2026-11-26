import ipywidgets as widgets

notes_box = widgets.Textarea(
    value=sample_notes,
    description="Notes:",
    layout=widgets.Layout(width="95%", height="170px"),
    style={"description_width": "initial"},
)

mode_box = widgets.ToggleButtons(
    options=[("Offline", "offline"), ("GEMINI FLASH 3.0", "live")],
    value="offline",
    description="Mode:",
)

button = widgets.Button(
    description="Extract action items", 
    button_style="primary", 
    icon="check"
)

output = widgets.Output()

def on_extract_clicked(_):
    with output:
        output.clear_output()
        text = notes_box.value.strip()
        if not text:
            print("Please enter meeting notes first.")
            return

        print("Mode:", "OFFLINE" if mode_box.value == "offline" else "LIVE GEMINI API")
        try:
            actions = offline_extract(text) if mode_box.value == "offline" else live_extract(text)
        except Exception as exc:
            # Keep raw provider errors and credentials off the shared screen
            print(f"Could not extract items ({type(exc).__name__}). Check setup and try again.")
            return

        if not actions:
            print("No actions found. In offline mode, use: Name: task by deadline")
            return

        for i, action in enumerate(actions, 1):
            print(f"\n{i}. {action['task']}")
            print(f"   Owner: {action['owner']} | Due: {action['deadline']}")

        print("\nReview every item against the original notes before using it.")

button.on_click(on_extract_clicked)
display(widgets.VBox([notes_box, mode_box, button, output]))
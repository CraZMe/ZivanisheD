GUI = '''

<TooltipMDFloatingButton@MDFloatingActionButton+MDTooltip>
<HoverButton@HoverBehavior+MDRectangleFlatIconButton>

MDScreen:
    md_bg_color: 0.945, 0.968, 0.929, 1
    
    MDDropDownItem:
        id: line_style
        pos_hint: {"center_x": .25, "center_y": .3}
        text: 'Line Style [ ]'
        on_release: app.line_style_menu.open()

    MDTextField:
        id: line_width
        pos_hint: {"center_x": .25, "center_y": .15}
        hint_text:  'Line Width'
        width: 120
        size_hint_x: None
        max_text_length:    2
        on_text_validate: app.set_line_width(self)
        line_color_focus: 0.568, 0.78, 0.694, 1
        color_mode: "custom"

    MDDropDownItem:
        id: line_color
        pos_hint: {"center_x": .25, "center_y": .45}
        text: 'Line Color [ ]'
        on_release: app.line_color_menu.open()


    TooltipMDFloatingButton:
        icon: "camera-iris"
        md_bg_color: "#91C7B1"
        pos_hint: {"center_x": .75, "center_y": .65}
        tooltip_text: "Configure Camera"
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"
        on_release: app.ButtonAction_configure_camera()

    TooltipMDFloatingButton:
        icon: "radiobox-marked"
        md_bg_color: "#B33951"
        pos_hint: {"center_x": .5, "center_y": .65}
        tooltip_text: "Start Recording"
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"
        on_release: app.ButtonAction_start_recording()

    TooltipMDFloatingButton:
        icon: "video-input-component"
        md_bg_color: "#91C7B1"
        pos_hint: {"center_x": .25, "center_y": .65}
        tooltip_text: "Test Input"
        tooltip_bg_color: "#aaaaaa"
        tooltip_font_style: "Overline"
        on_release: app.ButtonAction_test_input()

    MDTextField:
        id: line_width
        pos_hint: {"center_x": .75, "center_y": .15}
        hint_text:  'Sample Rate'
        helper_text: "[FPS]"
        helper_text_mode: "on_focus"
        width: 120
        size_hint_x: None
        on_text_validate: app.set_line_width(self)
        line_color_focus: 0.568, 0.78, 0.694, 1
        color_mode: "custom"

    HoverButton:
        id: directory_chooser
        icon:   "folder"
        pos_hint: {"center_x": .75, "center_y": .45}
        text: "DIRECTORY"
        width: 100
        size_hint_x: None
        text_color: "#808080"
        line_color: "#808080"
        icon_color: "#808080"
        on_release: app.ButtonAction_choose_directory()
        on_enter:   self.text_color = "#91C7B1"; self.line_color = "#91C7B1"; self.icon_color = "#91C7B1"
        on_leave:   self.text_color = "#808080"; self.line_color = "#808080"; self.icon_color = "#808080"
        
        

'''
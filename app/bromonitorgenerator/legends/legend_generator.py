from bromonitorgenerator.utils.colours import colours_dict


def __generate_row(text, colour):
    return f"""
            <tr>
                <td style="padding: 5px 10px; 
                border: 1px solid white; width:20px; height:20px; background: white;">
                <span style="margin:0 auto; background-color:{colour};
                height:15px; width:15px; display:block;"></span></td>
                <td style="padding: 5px 10px; 
                border: 1px solid white; background: white;">{text}</td>
            </tr>
            """


def __generate_legend(name, legend_items, ):
    html = '<table class="bromonitor-legend">'
    for item in legend_items:
        html = html + __generate_row(item, legend_items[item])
    html = html + "</table>"
    return html


def generate_quality_regime_legend():
    legend_items = {
        """Heeft één of meerdere gegevens in
          IMBRO-regime geregistreerd""": colours_dict["IMBRO"],
        """Heeft enkel gegevens in
          IMBRO/A-regime geregistreerd""": colours_dict["IMBRO/A"],
        "Heeft geen gegevens geregistreerd": colours_dict["Geen"]
    }
    return __generate_legend("Legenda voor kwaliteitsregimes landkaart",
                             legend_items)


def generate_object_type_legend():
    legend_items = {
        """Heeft één of meerdere grondwaterstandmetingen geregistreerd""": colours_dict["GLD"],
        "Heeft één of meerdere gegevens geregistreerd": colours_dict["CPT+GMW"],
        "Heeft geen gegevens geregistreerd": colours_dict["Geen"]
    }
    return __generate_legend("Legenda voor objecttypen landkaart",
                             legend_items)

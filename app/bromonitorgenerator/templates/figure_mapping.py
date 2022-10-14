import os
from bromonitorgenerator.visualisations.linegraphs import generate_line_graph
from bromonitorgenerator.visualisations.tables import (
    document_type_table_data,
    generate_top20_as_html,
    registrations_per_year,
    generate_top20_since_date_as_html,
    generate_gld_since_date_as_html,
    gld_registrations_and_supplements,
)
from bromonitorgenerator.visualisations.choropleths import (
    municipality_object_types,
    municipality_quality_regimes,
    province_object_types,
    province_quality_regimes,
    waterschap_object_types,
    waterschap_quality_regimes,
)
from bromonitorgenerator.visualisations.delta_report import generate_deltas_figure
from bromonitorgenerator.legends.legend_generator import (
    generate_object_type_legend,
    generate_quality_regime_legend,
)
from bromonitorgenerator.utils.utils import (
    get_bromonitor_sources,
    pretty_print_today,
    pretty_print_datetime,
)
from bromonitorgenerator.visualisations.barchart import generate_barchart
from bromonitorgenerator.utils.documentTypes import init_document_registries
from bromonitorgenerator.utils.start_date import get_start_date, get_new_start_date
from bromonitorgenerator.visualisations.tables_acc import (
    generate_barchart_table,
    generate_data_bronhouder_type,
    generate_line_graph_table,
    generate_deltas_table,
    get_number_of_bronhouders,
    table_quality_regime_map,
    table_object_type_map,
    generate_table_bronhouder_permaand,
)
from bromonitorgenerator.visualisations.animated_graphs import (
    generate_linechart_bronhouder_permaand,
)

from bromonitorgenerator.utils.get_static_data import get_total_registered_objects, parse_weekly_top20

# Load the document type registry as retrieved from the bromonitor backend
init_document_registries()

figure_mapping = {    
    "wekelijkse_delta": generate_deltas_figure(),
    "wekelijkse_delta_tabel": generate_deltas_table(),
    "typenoverzicht": document_type_table_data(),
    "datumstempel": pretty_print_today(),
    "bronvermelding": get_bromonitor_sources(),
    "documenttypen_staafgrafiek": generate_barchart(),
    "documenttypen_tabel": generate_barchart_table(),
    "documenttypen_gemeentekaart": municipality_object_types(),
    "documenttypen_provinciekaart": province_object_types(),
    "documenttypen_legenda": generate_object_type_legend(),
    "documenttypen_waterschapkaart": waterschap_object_types(),
    "documenttypen_gemeentetabel": table_object_type_map("Gemeente"),
    "documenttypen_waterschaptabel": table_object_type_map("Waterschap"),
    "documenttypen_provincietabel": table_object_type_map("Provincie"),
    "kwaliteitsregimes_gemeentekaart": municipality_quality_regimes(),
    "kwaliteitsregimes_provinciekaart": province_quality_regimes(),
    "kwaliteitsregimes_waterschapkaart": waterschap_quality_regimes(),
    "kwaliteitsregimes_gemeentetabel": table_quality_regime_map("Gemeente"),
    "kwaliteitsregimes_waterschaptabel": table_quality_regime_map("Waterschap"),
    "kwaliteitsregimes_provincietabel": table_quality_regime_map("Provincie"),
    "kwaliteitsregimes_legenda": generate_quality_regime_legend(),
    "registratieobjecten_top20": generate_top20_as_html(),
    "grondwatermonitoringputten_top20": generate_top20_as_html(
        "Grondwatermonitoringput"
    ),
    "cpt_top20": generate_top20_as_html("GeotechnischSondeeronderzoek"),
    "cpt_jaren": generate_line_graph("GeotechnischSondeeronderzoek"),
    "bhrp_jaren": generate_line_graph("BodemkundigBooronderzoek"),
    "sfr_jaren": generate_line_graph("BodemkundigWandonderzoek"),
    "bhrgt_jaren": generate_line_graph("GeotechnischBooronderzoek"),
    "gmn_jaren": generate_line_graph("Grondwatermonitoringnet"),
    "gmw_jaren": generate_line_graph("Grondwatermonitoringput"),
    "gld_jaren": generate_line_graph("Grondwaterstandonderzoek"),
    "cpt_jaren_tabel": generate_line_graph_table(
        "GeotechnischSondeeronderzoek", "CPT's"
    ),
    "bhrp_jaren_tabel": generate_line_graph_table(
        "BodemkundigBooronderzoek", "BHR-P's"
    ),
    "sfr_jaren_tabel": generate_line_graph_table(
        "BodemkundigWandonderzoek", "SFR's"
    ),
    "bhrgt_jaren_tabel": generate_line_graph_table(
        "GeotechnischBooronderzoek", "BHR-GT's"
    ),
    "gmn_jaren_tabel": generate_line_graph_table(
        "Grondwatermonitoringnet", "GMN's"
    ),
    "gmw_jaren_tabel": generate_line_graph_table("Grondwatermonitoringput", "GMW's"),
    "gld_jaren_tabel": generate_line_graph_table(
        "Grondwaterstandonderzoek", "GLD's"
    ),
    "wekelijkse_top20": generate_top20_since_date_as_html(),
    "gld_delta": generate_gld_since_date_as_html(),
    "startdatum": pretty_print_datetime(get_start_date()),
    "startdatum_nieuw": pretty_print_datetime(get_new_start_date()),
    "gld_top_20": gld_registrations_and_supplements(),
    "maandlijkse_bronhouder_table": generate_table_bronhouder_permaand(),
    "bewegend_bronhouders": generate_linechart_bronhouder_permaand(),
    "base_url": os.environ.get("baseUrl", "http://localhost:8080"),
}

data ={
    "datumstempel": pretty_print_today(),
    "data_gemeente_typen": generate_data_bronhouder_type("Gemeente", "objecttypen"),
    "data_gemeente_regimes": generate_data_bronhouder_type("Gemeente", "kwaliteitsregimes"),
    "data_provincie_typen": generate_data_bronhouder_type("Provincie", "objecttypen"),
    "data_provincie_regimes": generate_data_bronhouder_type("Provincie", "kwaliteitsregimes"),
    "data_waterschap_typen": generate_data_bronhouder_type("Waterschap", "objecttypen"),
    "data_waterschap_regimes": generate_data_bronhouder_type("Waterschap", "kwaliteitsregimes"),
}

data["aantal_gemeenten"] = get_number_of_bronhouders(data["data_gemeente_typen"]),
data["aantal_provincies"] = get_number_of_bronhouders(data["data_provincie_typen"]),
data["aantal_waterschappen"] = get_number_of_bronhouders(data["data_waterschap_typen"]),

parsed_wekelijkse_top20 = parse_weekly_top20(figure_mapping["wekelijkse_top20"])

data["totaal_aantal_objecten"] = get_total_registered_objects(figure_mapping["documenttypen_tabel"])
data["aantal_bronhouders"] = parsed_wekelijkse_top20["bronhouders"]
data["aantal_registraties"] = parsed_wekelijkse_top20["registraties"]
data["aantal_glds"] = parsed_wekelijkse_top20["glds"]
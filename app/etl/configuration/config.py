registration_types = []


class JoinTableDefinition:
    """Object holding a table that should be joinedloaded into its parent
    and a list of nested JoinTableDefinitions that should be joinedloaded
    into this specific object.
    """

    def __init__(self, table_name, inner_joins):
        self.table_name = table_name
        self.inner_joins = inner_joins


class RegistrationTypeConfig:
    """Object holding all the configuration values needed
    for a registration type during ETL.
    """

    def __init__(
        self, type_name, full_name, main_table, pk_col, mongo_collection, sourceKey
    ):
        self.type_name = type_name
        self.full_name = full_name
        self.main_table = main_table
        self.pk_col = pk_col
        self.mongo_collection = mongo_collection
        self.location_table = None
        self.registration_history_table = None
        self.join_tables = []
        self.sourceKey = sourceKey

    def set_location_table(self, location_table):
        self.location_table = location_table

    def set_registration_history_table(self, registration_history_table):
        self.registration_history_table = registration_history_table

    def set_join_tables(self, join_tables):
        for jt in join_tables:
            self.join_tables.append(jt)


def init_registration_types():
    # Init gmw
    gmw = RegistrationTypeConfig(
        type_name="gmw",
        full_name="Grondwatermonitoringput",
        main_table="gmw_monitoring_well",
        pk_col="monitoring_well_id",
        mongo_collection="specificGMW",
        sourceKey="sourceGMW",
    )
    gmw.set_join_tables(
        [
            JoinTableDefinition(
                "gmw_monitoring_tube_collection",
                [
                    JoinTableDefinition(
                        "gmw_geo_ohm_cable_collection",
                        [JoinTableDefinition("gmw_electrode_collection", [])],
                    )
                ],
            )
        ]
    )
    registration_types.append(gmw)

    # Init sfr
    sfr = RegistrationTypeConfig(
        type_name="sfr",
        full_name="BodemkundigWandonderzoek",
        main_table="soil_face_research",
        pk_col="soil_face_research_pk",
        mongo_collection="specificSFR",
        sourceKey="sourceSFR",
    )
    sfr.set_location_table("deliveredLocationCollection")
    sfr.set_registration_history_table("registrationHistoryCollection")
    sfr.set_join_tables(
        [
            JoinTableDefinition("delivered_location_collection", []),
            JoinTableDefinition("registration_history_collection", []),
        ]
    )
    registration_types.append(sfr)

    # Init cpt
    cpt = RegistrationTypeConfig(
        type_name="cpt",
        full_name="GeotechnischSondeeronderzoek",
        main_table="cpt_geotechnical_survey",
        pk_col="geotechnical_survey_id",
        mongo_collection="specificCPT",
        sourceKey="sourceCPT",
    )
    cpt.set_join_tables(
        [
            JoinTableDefinition(
                "cpt_cone_penetrometer_survey_collection",
                [JoinTableDefinition("cpt_cone_penetration_test_collection", [])],
            )
        ]
    )
    registration_types.append(cpt)

    # Init bhr-gt
    bhrgt = RegistrationTypeConfig(
        type_name="bhr-gt",
        full_name="GeotechnischBooronderzoek",
        main_table="borehole_research",
        pk_col="borehole_research_pk",
        mongo_collection="specificBHRGT",
        sourceKey="sourceBHRGT",
    )
    bhrgt.set_location_table("deliveredLocationCollection")
    bhrgt.set_registration_history_table("registrationHistoryCollection")
    bhrgt.set_join_tables(
        [
            JoinTableDefinition("boring_collection", []),
            JoinTableDefinition("registration_history_collection", []),
            JoinTableDefinition("delivered_location_collection", []),
        ]
    )
    registration_types.append(bhrgt)

    # Init bhr-p
    bhrp = RegistrationTypeConfig(
        type_name="bhr-p",
        full_name="BodemkundigBooronderzoek",
        main_table="borehole_research",
        pk_col="borehole_research_pk",
        mongo_collection="specificBHR",
        sourceKey="sourceBHRP",
    )
    bhrp.set_location_table("deliveredLocationCollection")
    bhrp.set_registration_history_table("registrationHistoryCollection")
    bhrp.set_join_tables(
        [
            JoinTableDefinition("delivered_location_collection", []),
            JoinTableDefinition("registration_history_collection", []),
        ]
    )
    registration_types.append(bhrp)

    # Init gmn
    gmn = RegistrationTypeConfig(
        type_name="gmn",
        full_name="Grondwatermonitoringnet",
        main_table="groundwater_monitoring_net",
        pk_col="groundwater_monitoring_net_pk",
        mongo_collection="specificGMN",
        sourceKey="sourceGMN",
    )
    gmn.set_registration_history_table("registrationHistoryCollection")
    gmn.set_join_tables(
        [
            JoinTableDefinition("registration_history_collection", []),
            JoinTableDefinition(
                "measuring_point_with_history_collection",
                [JoinTableDefinition("groundwater_monitoring_tube_collection", [])],
            ),
        ]
    )
    registration_types.append(gmn)

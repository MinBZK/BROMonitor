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
        main_table="gm_gmw",
        pk_col="gm_gmw_pk",
        mongo_collection="specificGMW",
        sourceKey="source_GMW_GMN_GLD",
    )
    gmw.set_join_tables(
        [
            JoinTableDefinition("gm_gmw_monitoringtube_collection",[])
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
        main_table="geotechnical_cpt_survey",
        pk_col="geotechnical_cpt_survey_pk",
        mongo_collection="specificCPT",
        sourceKey="sourceCPT",
    )
    cpt.set_registration_history_table("registrationHistoryCollection")
    cpt.set_join_tables(
        [
            JoinTableDefinition("registration_history_collection", []),
            JoinTableDefinition(
                "cone_penetrometer_survey_collection",
                [JoinTableDefinition("cone_penetration_test_collection", [])],
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
        main_table="gm_gmn",
        pk_col="gm_gmn_pk",
        mongo_collection="specificGMN",
        sourceKey="source_GMW_GMN_GLD",
    )
    gmn.set_join_tables(
        [
            JoinTableDefinition(
                "gm_gmn_measuringpoint_collection",
                [
                    JoinTableDefinition("gm_gmw_monitoringtube_collection", [])
                ],
            ),
        ]
    )
    registration_types.append(gmn)

    # Init gld
    gld = RegistrationTypeConfig(
        type_name="gld",
        full_name="Grondwaterstandonderzoek",
        main_table="gm_gld",
        pk_col="gm_gld_pk",
        mongo_collection="specificGLD",
        sourceKey="source_GMW_GMN_GLD",
    )
    gld.set_join_tables(
        [
            JoinTableDefinition("gm_gmw_monitoringtube_collection", []),
        ]
    )
    registration_types.append(gld)

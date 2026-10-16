# ============================================================
# DEPTH-SPECIFIC SCIENTIFIC INFORMATION
# The Ocean Descent
# ============================================================


DEPTH_ZONES = [

    {
        "min": 0,
        "max": 50,

        "name": "Surface Ocean",

        "short_description": """
        The surface ocean is directly connected to the atmosphere.
        Sunlight, wind, rainfall and evaporation strongly influence
        its temperature and salinity.
        """,

        "physical": """
        This region receives sunlight and is often strongly mixed by
        wind and waves. Temperature can vary considerably with weather
        and season.
        """,

        "chemistry": """
        The surface ocean exchanges gases such as oxygen and carbon
        dioxide with the atmosphere. Nutrient availability helps
        control biological productivity.
        """,

        "life": """
        Sunlight allows phytoplankton to perform photosynthesis.
        Zooplankton, fish and many other organisms depend directly or
        indirectly on this biological production.
        """,

        "geology": """
        Compared with deep ocean environments, the surface is dominated
        by atmospheric and biological processes rather than extreme
        pressure.
        """,

        "measurement": """
        CTDs measure temperature, conductivity and pressure as they
        descend through the water column. Salinity is calculated from
        conductivity, temperature and pressure.
        """,

        "facts": [
            "Sunlight provides the energy that drives marine photosynthesis.",
            "The surface ocean exchanges heat and gases with the atmosphere.",
            "Wind-driven mixing can transport heat, salt and oxygen downward.",
            "Phytoplankton form the base of many marine food webs."
        ]
    },


    {
        "min": 50,
        "max": 200,

        "name": "Sunlight Zone",

        "short_description": """
        Sunlight still penetrates this region, although light decreases
        rapidly with depth.
        """,

        "physical": """
        Temperature and salinity begin to reflect the transition from
        the surface mixed layer toward deeper water.
        """,

        "chemistry": """
        Photosynthesis remains possible, but the amount of available
        light decreases rapidly with depth.
        """,

        "life": """
        Phytoplankton and zooplankton are abundant compared with the
        deep ocean. Many organisms depend on material produced here.
        """,

        "geology": """
        Sinking biological particles begin their journey toward the
        deep ocean from this region.
        """,

        "measurement": """
        CTDs provide continuous measurements as they descend, allowing
        scientists to identify changes in temperature and salinity
        with depth.
        """,

        "facts": [
            "Most oceanic primary production occurs in the sunlit surface ocean.",
            "Light intensity decreases dramatically with depth.",
            "Organic particles produced near the surface can eventually reach the deep sea.",
            "Temperature and salinity influence seawater density."
        ]
    },


    {
        "min": 200,
        "max": 1000,

        "name": "Twilight Zone",

        "short_description": """
        Only a small amount of sunlight reaches the twilight zone.
        Photosynthesis becomes increasingly difficult with depth.
        """,

        "physical": """
        Temperature commonly decreases rapidly through part of this
        depth range. This transition is associated with the thermocline.
        """,

        "chemistry": """
        Organic material produced near the surface sinks into this
        region. Microbial decomposition transforms organic matter and
        affects the cycling of carbon and nutrients.
        """,

        "life": """
        This is an extremely active region biologically. Many animals
        migrate upward at night to feed and return to deeper water
        during the day.
        """,

        "geology": """
        Sinking particles transport material from the surface ecosystem
        toward deeper parts of the ocean.
        """,

        "measurement": """
        CTD profiles are particularly useful here because rapid changes
        in temperature and salinity can reveal boundaries between
        different water masses.
        """,

        "facts": [
            "Many animals perform daily vertical migrations through this zone.",
            "Very little sunlight reaches the deeper part of the twilight zone.",
            "Sinking organic particles transport carbon downward.",
            "The thermocline can create strong vertical density gradients."
        ]
    },


    {
        "min": 1000,
        "max": 2000,

        "name": "Upper Midnight Zone",

        "short_description": """
        Below about 1,000 m, sunlight is essentially absent. The ocean
        becomes permanently dark.
        """,

        "physical": """
        Temperatures are much lower than at the surface and pressure
        is already around one hundred times atmospheric pressure.
        """,

        "chemistry": """
        There is no significant photosynthesis. Organic material arriving
        from above becomes an important source of energy and carbon.
        """,

        "life": """
        Animals living here are adapted to darkness, high pressure and
        limited food. Bioluminescence is common among many deep-sea
        organisms.
        """,

        "geology": """
        Marine snow — small particles of organic and inorganic material —
        continually sinks through the water column.
        """,

        "measurement": """
        CTDs measure temperature, conductivity and pressure directly
        during the descent. These observations help identify deep water
        masses and their physical properties.
        """,

        "facts": [
            "Sunlight is essentially absent.",
            "Bioluminescence is widespread among deep-sea organisms.",
            "Pressure is roughly 100 times atmospheric pressure around 1,000 m.",
            "Sinking particles provide an important food source."
        ]
    },


    {
        "min": 2000,
        "max": 4000,

        "name": "Deep Ocean",

        "short_description": """
        This is the deep, permanently dark ocean. Temperatures are low
        and pressure is hundreds of times greater than at the surface.
        """,

        "physical": """
        Deep water properties change much more gradually than in the
        upper ocean. Small differences in temperature and salinity can
        still affect density and circulation.
        """,

        "chemistry": """
        Microbial decomposition of sinking organic matter influences
        dissolved carbon, oxygen and nutrients.
        """,

        "life": """
        Deep-sea animals survive with very little food and no sunlight.
        Many feed on particles, detritus or other organisms.
        """,

        "geology": """
        Material transported from the surface can eventually settle
        onto the seafloor, contributing to deep-ocean sediments.
        """,

        "measurement": """
        Deep CTD casts allow scientists to measure the physical
        properties of water masses thousands of metres below the surface.
        """,

        "facts": [
            "The deep ocean contains most of the ocean's volume.",
            "No sunlight is available for photosynthesis.",
            "Pressure continues to increase by roughly one atmosphere per 10 m.",
            "Deep water is an important component of global ocean circulation."
        ]
    },


    {
        "min": 4000,
        "max": 6000,

        "name": "Abyssal Zone",

        "short_description": """
        The abyssal ocean is extremely cold, dark and under enormous
        pressure.
        """,

        "physical": """
        Temperatures are commonly close to the freezing point of
        seawater. Water movement is influenced by large-scale
        circulation and seafloor topography.
        """,

        "chemistry": """
        Oxygen and nutrients are redistributed by circulation and by
        the decomposition of sinking organic material.
        """,

        "life": """
        Life is sparse compared with the surface but remains diverse.
        Microbes and animals have adaptations for extreme pressure,
        darkness and low food availability.
        """,

        "geology": """
        The seafloor contains sediments accumulated over long periods.
        Topography can redirect deep currents and sediment transport.
        """,

        "measurement": """
        Reaching these depths requires specialized deep-ocean CTD
        systems and pressure-rated equipment.
        """,

        "facts": [
            "Pressure at 4,000 m is roughly 400 times surface atmospheric pressure.",
            "Abyssal waters are among the coldest large habitats on Earth.",
            "Deep circulation transports heat, salt, oxygen and nutrients.",
            "Most of this environment receives no sunlight."
        ]
    },


    {
        "min": 6000,
        "max": 8000,

        "name": "Upper Hadal Zone",

        "short_description": """
        At 6,000 m you enter the hadal zone — the part of the ocean
        found primarily inside deep trenches.
        """,

        "physical": """
        Pressure is extreme and temperatures remain very low. Trenches
        can have circulation patterns that differ from the surrounding
        abyssal ocean.
        """,

        "chemistry": """
        Organic particles and sediments can be concentrated by the
        steep slopes and geometry of trenches.
        """,

        "life": """
        Hadal organisms include specialized amphipods, holothurians,
        polychaetes and microorganisms adapted to extreme pressure.
        """,

        "geology": """
        Ocean trenches form where one tectonic plate is forced beneath
        another at a subduction zone.
        """,

        "measurement": """
        Scientific measurements at these depths require instruments
        capable of operating under hundreds of atmospheres of pressure.
        """,

        "facts": [
            "The hadal zone begins at approximately 6,000 m.",
            "Hadal environments occur mainly in ocean trenches.",
            "Extreme pressure strongly affects biological and chemical processes.",
            "Trench topography can concentrate sinking particles."
        ]
    },


    {
        "min": 8000,
        "max": 10000,

        "name": "Deep Hadal Zone",

        "short_description": """
        This is one of the most extreme environments on Earth:
        completely dark, extremely cold and under enormous pressure.
        """,

        "physical": """
        Pressure approaches 1,000 atmospheres. Water properties are
        influenced by deep circulation and the complex geometry of
        the Mariana Trench.
        """,

        "chemistry": """
        Sediment accumulation and decomposition of organic matter can
        create distinct chemical environments within the trench.
        """,

        "life": """
        Life persists despite the pressure. Microbial communities and
        specialized hadal animals have evolved mechanisms that allow
        them to function under extreme pressure.
        """,

        "geology": """
        The Mariana Trench is associated with subduction, where the
        Pacific Plate descends beneath the Philippine Sea Plate.
        """,

        "measurement": """
        Deep CTD instruments are lowered carefully through the water
        column. The 2024 Jiang dataset includes observations reaching
        approximately 10.85 km.
        """,

        "facts": [
            "Pressure is approaching 1,000 atmospheres.",
            "No sunlight reaches this environment.",
            "The trench is a tectonically active subduction environment.",
            "Specialized organisms can survive these pressures."
        ]
    },


    {
        "min": 10000,
        "max": 11000,

        "name": "Challenger Deep",

        "short_description": """
        You are now at the deepest part of the Mariana Trench and
        approximately 10.85 km below sea level.
        """,

        "physical": """
        Challenger Deep is extremely cold and experiences pressures
        exceeding 1,000 times atmospheric pressure.
        """,

        "chemistry": """
        Chemical conditions are influenced by deep circulation,
        sediment accumulation and the decomposition of organic matter
        delivered from shallower waters.
        """,

        "life": """
        Despite the extreme pressure and darkness, life has been
        observed at Challenger Deep. Microorganisms and specialized
        animals can survive under these conditions.
        """,

        "geology": """
        Challenger Deep lies within the Mariana Trench, one of Earth's
        deepest subduction-related features.
        """,

        "measurement": """
        The CTD profile used here reaches approximately 10,850 m.
        Measurements at these depths require highly pressure-resistant
        scientific instruments.
        """,

        "facts": [
            "The profile reaches approximately 10,850 m.",
            "Pressure exceeds 1,000 times atmospheric pressure.",
            "Challenger Deep is deeper than Mount Everest is tall.",
            "The water remains liquid despite the enormous pressure.",
            "The hadal environment supports specialized biological communities."
        ]
    }
]


def get_depth_information(depth):
    """
    Return the scientific information corresponding to a depth.
    """

    for zone in DEPTH_ZONES:

        if zone["min"] <= depth < zone["max"]:
            return zone

    # Handle the very deepest endpoint
    return DEPTH_ZONES[-1]

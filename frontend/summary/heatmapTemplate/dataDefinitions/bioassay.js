import {
    COLORS,
    defineAxis,
    defineFilter,
    defineMultiAxis,
    defineProps,
    defineTable,
} from "./shared";

// BSD = bioassay study design
const BSD = {
        studyId: defineProps("studyId", "Study ID", "study id"),
        studyCitation: defineProps("studyCitation", "Study citation", "study citation"),
        studyIdentifier: defineProps("studyIdentifier", "Study identifier", "study identifier"),
        studyEval: defineProps("studyEval", "Overall study evaluation", "overall study evaluation"),
        experimentType: defineProps("experimentType", "Study design", "experiment type"),
        species: defineProps("species", "Species", "species"),
        strain: defineProps("strain", "Strain", "strain"),
        routeOfExposure: defineProps("routeOfExposure", "Route of exposure", "route of exposure"),
        experimentChemical: defineProps("experimentChemical", "Chemical", "experiment chemical"),
        sex: defineProps("sex", "Sex", "sex"),
        system: defineProps("system", "System", "system"),
        organ: defineProps("organ", "Organ", "organ"),
        effect: defineProps("effect", "Effect", "effect"),
        diagnostic: defineProps("diagnostic", "Diagnostic", "diagnostic"),
        doseUnits: defineProps("doseUnits", "Dose units", "dose units"),
    },
    BSDSettings = {
        AXIS_OPTIONS: {
            studyCitation: defineAxis(BSD.studyCitation),
            studyEval: defineAxis(BSD.studyEval, {delimiter: "|"}),
            doseUnits: defineAxis(BSD.doseUnits, {delimiter: "|"}),
            experimentType: defineAxis(BSD.experimentType, {delimiter: "|"}),
            routeOfExposure: defineAxis(BSD.routeOfExposure, {delimiter: "|"}),
            experimentChemical: defineAxis(BSD.experimentChemical, {delimiter: "|"}),
            speciesSex: defineMultiAxis([BSD.species, BSD.sex], "speciesSex", "Species & sex", {
                delimiter: "|",
            }),
            speciesStrain: defineMultiAxis(
                [BSD.species, BSD.strain],
                "speciesStrain",
                "Species & strain",
                {delimiter: "|"}
            ),
            system: defineAxis(BSD.system, {delimiter: "|"}),
            organ: defineAxis(BSD.organ, {delimiter: "|"}),
            effect: defineAxis(BSD.effect, {delimiter: "|"}),
            diagnostic: defineAxis(BSD.diagnostic, {delimiter: "|"}),
        },
        FILTER_OPTIONS: {
            studyCitation: defineFilter(BSD.studyCitation, {on_click_event: "study"}),
            studyIdentifier: defineFilter(BSD.studyIdentifier, {on_click_event: "study"}),
            studyEval: defineFilter(BSD.studyEval, {delimiter: "|"}),
            experimentType: defineFilter(BSD.experimentType, {delimiter: "|"}),
            species: defineFilter(BSD.species, {delimiter: "|"}),
            strain: defineFilter(BSD.strain, {delimiter: "|"}),
            routeOfExposure: defineFilter(BSD.routeOfExposure, {delimiter: "|"}),
            experimentChemical: defineFilter(BSD.experimentChemical, {delimiter: "|"}),
            sex: defineFilter(BSD.sex, {delimiter: "|"}),
            system: defineFilter(BSD.system, {delimiter: "|"}),
            organ: defineFilter(BSD.organ, {delimiter: "|"}),
            effect: defineFilter(BSD.effect, {delimiter: "|"}),
            diagnostic: defineFilter(BSD.diagnostic, {delimiter: "|"}),
            doseUnits: defineFilter(BSD.doseUnits, {delimiter: "|"}),
        },
        TABLE_FIELDS: {
            studyCitation: defineTable(BSD.studyCitation, {on_click_event: "study"}),
            studyIdentifier: defineTable(BSD.studyIdentifier, {on_click_event: "study"}),
            studyEval: defineTable(BSD.studyEval, {delimiter: "|"}),
            experimentType: defineTable(BSD.experimentType, {delimiter: "|"}),
            species: defineTable(BSD.species, {delimiter: "|"}),
            strain: defineTable(BSD.strain, {delimiter: "|"}),
            routeOfExposure: defineTable(BSD.routeOfExposure, {delimiter: "|"}),
            experimentChemical: defineTable(BSD.experimentChemical, {delimiter: "|"}),
            sex: defineTable(BSD.sex, {delimiter: "|"}),
            system: defineTable(BSD.system, {delimiter: "|"}),
            organ: defineTable(BSD.organ, {delimiter: "|"}),
            effect: defineTable(BSD.effect, {delimiter: "|"}),
            diagnostic: defineTable(BSD.diagnostic, {delimiter: "|"}),
            doseUnits: defineTable(BSD.doseUnits, {delimiter: "|"}),
        },
        DASHBOARDS: [],
    };

// define dashboards after building-blocks are defined
BSDSettings.DASHBOARDS = [
    {
        id: "study design vs. system",
        label: "study design vs. system",
        upperColor: COLORS.blue,
        x_axis: BSDSettings.AXIS_OPTIONS.experimentType.id,
        y_axis: BSDSettings.AXIS_OPTIONS.system.id,
        filters: [
            BSDSettings.FILTER_OPTIONS.studyCitation.id,
            BSDSettings.FILTER_OPTIONS.routeOfExposure.id,
            BSDSettings.FILTER_OPTIONS.experimentChemical.id,
            BSDSettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BSDSettings.TABLE_FIELDS.studyCitation.id,
            BSDSettings.TABLE_FIELDS.species.id,
            BSDSettings.TABLE_FIELDS.sex.id,
            BSDSettings.TABLE_FIELDS.system.id,
            BSDSettings.TABLE_FIELDS.organ.id,
            BSDSettings.TABLE_FIELDS.effect.id,
        ],
    },
    {
        id: "test subject vs. system",
        label: "test subject vs. system",
        upperColor: COLORS.red,
        x_axis: BSDSettings.AXIS_OPTIONS.speciesSex.id,
        y_axis: BSDSettings.AXIS_OPTIONS.system.id,
        filters: [
            BSDSettings.FILTER_OPTIONS.studyCitation.id,
            BSDSettings.FILTER_OPTIONS.experimentType.id,
            BSDSettings.FILTER_OPTIONS.experimentChemical.id,
            BSDSettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BSDSettings.TABLE_FIELDS.studyCitation.id,
            BSDSettings.TABLE_FIELDS.experimentType.id,
            BSDSettings.TABLE_FIELDS.routeOfExposure.id,
            BSDSettings.TABLE_FIELDS.experimentChemical.id,
            BSDSettings.TABLE_FIELDS.system.id,
            BSDSettings.TABLE_FIELDS.organ.id,
            BSDSettings.TABLE_FIELDS.effect.id,
        ],
    },
    {
        id: "system vs. study citation",
        label: "system vs. study citation",
        upperColor: COLORS.green,
        x_axis: BSDSettings.AXIS_OPTIONS.system.id,
        y_axis: BSDSettings.AXIS_OPTIONS.studyCitation.id,
        filters: [],
        table_fields: [
            BSDSettings.TABLE_FIELDS.studyCitation.id,
            BSDSettings.TABLE_FIELDS.experimentType.id,
            BSDSettings.TABLE_FIELDS.species.id,
            BSDSettings.TABLE_FIELDS.strain.id,
            BSDSettings.TABLE_FIELDS.sex.id,
            BSDSettings.TABLE_FIELDS.routeOfExposure.id,
            BSDSettings.TABLE_FIELDS.experimentChemical.id,
            BSDSettings.TABLE_FIELDS.system.id,
            BSDSettings.TABLE_FIELDS.organ.id,
            BSDSettings.TABLE_FIELDS.effect.id,
        ],
    },
    {
        id: "chemical vs. study citation",
        label: "chemical vs. study citation",
        upperColor: COLORS.orange,
        x_axis: BSDSettings.AXIS_OPTIONS.experimentChemical.id,
        y_axis: BSDSettings.AXIS_OPTIONS.studyCitation.id,
        filters: [
            BSDSettings.FILTER_OPTIONS.experimentType.id,
            BSDSettings.FILTER_OPTIONS.routeOfExposure.id,
            BSDSettings.FILTER_OPTIONS.system.id,
        ],
        table_fields: [
            BSDSettings.TABLE_FIELDS.studyCitation.id,
            BSDSettings.TABLE_FIELDS.species.id,
            BSDSettings.TABLE_FIELDS.sex.id,
            BSDSettings.TABLE_FIELDS.system.id,
            BSDSettings.TABLE_FIELDS.organ.id,
            BSDSettings.TABLE_FIELDS.effect.id,
        ],
    },
    {
        id: "dose units vs. study citation",
        label: "dose units vs. study citation",
        upperColor: COLORS.purple,
        x_axis: BSDSettings.AXIS_OPTIONS.doseUnits.id,
        y_axis: BSDSettings.AXIS_OPTIONS.studyCitation.id,
        filters: [
            BSDSettings.FILTER_OPTIONS.experimentType.id,
            BSDSettings.FILTER_OPTIONS.routeOfExposure.id,
            BSDSettings.FILTER_OPTIONS.experimentChemical.id,
        ],
        table_fields: [
            BSDSettings.TABLE_FIELDS.studyCitation.id,
            BSDSettings.TABLE_FIELDS.species.id,
            BSDSettings.TABLE_FIELDS.sex.id,
            BSDSettings.TABLE_FIELDS.system.id,
            BSDSettings.TABLE_FIELDS.organ.id,
            BSDSettings.TABLE_FIELDS.effect.id,
            BSDSettings.TABLE_FIELDS.doseUnits.id,
        ],
    },
];

// BE = Bioassay endpoints
const BE = {
        studyId: defineProps("studyId", "Study id", "study id"),
        studyCitation: defineProps("studyCitation", "Study citation", "study citation"),
        studyIdentifier: defineProps("studyIdentifier", "Study identifier", "study identifier"),
        studyEval: defineProps("studyEval", "Overall study evaluation", "overall study evaluation"),
        experimentId: defineProps("experimentId", "Experiment id", "experiment id"),
        experimentName: defineProps("experimentName", "Experiment name", "experiment name"),
        experimentType: defineProps("experimentType", "Study design", "experiment type"),
        treatmentPeriod: defineProps("treatmentPeriod", "Treatment period", "treatment period"),
        experimentCas: defineProps("experimentCas", "Experiment CAS", "experiment cas"),
        chemical: defineProps("chemical", "Experiment chemical", "experiment chemical"),
        animalGroupId: defineProps("animalGroupId", "Animal group id", "animal group id"),
        animalGroupName: defineProps("animalGroupName", "Animal group name", "animal group name"),
        animalDesc: defineProps("animalDesc", "Animal description", "animal description"),
        animalDescN: defineProps(
            "animalDescN",
            "Animal description, with N",
            "animal description, with n"
        ),
        species: defineProps("species", "Species", "species"),
        strain: defineProps("strain", "Strain", "strain"),
        sex: defineProps("sex", "Sex", "sex"),
        generation: defineProps("generation", "Generation", "generation"),
        routeOfExposure: defineProps("routeOfExposure", "Route of exposure", "route of exposure"),
        endpointId: defineProps("endpointId", "Endpoint ID", "endpoint id"),
        system: defineProps("system", "System", "system"),
        organ: defineProps("organ", "Organ", "organ"),
        effect: defineProps("effect", "Effect", "effect"),
        effectSubtype: defineProps("effectSubtype", "Effect subtype", "effect subtype"),
        endpointName: defineProps("endpointName", "Endpoint name", "endpoint name"),
        diagnostic: defineProps("diagnostic", "Diagnostic", "diagnostic"),
        observationTime: defineProps("observationTime", "Observation time", "observation time"),
    },
    BESettings = {
        AXIS_OPTIONS: {
            studyCitation: defineAxis(BE.studyCitation),
            studyEval: defineAxis(BE.studyEval),
            speciesSex: defineMultiAxis([BE.species, BE.sex], "speciesSex", "Species & Sex"),
            experimentType: defineAxis(BE.experimentType),
            chemical: defineAxis(BE.chemical),
            routeOfExposure: defineAxis(BE.routeOfExposure),
            system: defineAxis(BE.system),
            organ: defineAxis(BE.organ),
            effect: defineAxis(BE.effect),
            systemOrgan: defineMultiAxis([BE.system, BE.organ], "systemOrgan", "System & organ"),
            experimentTypeSystem: defineMultiAxis(
                [BE.experimentType, BE.system],
                "experimentTypeSystem",
                "Study design & system"
            ),
            endpointName: defineAxis(BE.endpointName),
            diagnostic: defineAxis(BE.diagnostic),
        },
        FILTER_OPTIONS: {
            studyCitation: defineFilter(BE.studyCitation, {on_click_event: "study"}),
            studyEval: defineFilter(BE.studyEval),
            experimentType: defineFilter(BE.experimentType),
            species: defineFilter(BE.species),
            strain: defineFilter(BE.strain),
            sex: defineFilter(BE.sex),
            generation: defineFilter(BE.generation),
            system: defineFilter(BE.system),
            organ: defineFilter(BE.organ),
            effect: defineFilter(BE.effect),
            effectSubtype: defineFilter(BE.effectSubtype),
            endpointName: defineFilter(BE.endpointName),
            diagnostic: defineFilter(BE.diagnostic),
            observationTime: defineFilter(BE.observationTime),
        },
        TABLE_FIELDS: {
            studyCitation: defineTable(BE.studyCitation, {on_click_event: "study"}),
            studyEval: defineTable(BE.studyEval),
            experimentName: defineTable(BE.experimentName, {on_click_event: "experiment"}),
            treatmentPeriod: defineTable(BE.treatmentPeriod),
            animalGroupName: defineTable(BE.animalGroupName, {on_click_event: "animal_group"}),
            animalDesc: defineTable(BE.animalDesc, {on_click_event: "animal_group"}),
            animalDescN: defineTable(BE.animalDescN, {on_click_event: "animal_group"}),
            species: defineTable(BE.species),
            strain: defineTable(BE.strain),
            sex: defineTable(BE.sex),
            system: defineTable(BE.system),
            organ: defineTable(BE.organ),
            effect: defineTable(BE.effect),
            effectSubtype: defineTable(BE.effectSubtype),
            endpointName: defineTable(BE.endpointName, {on_click_event: "endpoint_complete"}),
            diagnostic: defineTable(BE.diagnostic),
            observationTime: defineTable(BE.observationTime),
        },
        DASHBOARDS: [],
    };

// define dashboards after building-blocks are defined
BESettings.DASHBOARDS = [
    {
        id: "system vs. test subject",
        label: "system vs. test subject",
        upperColor: COLORS.blue,
        x_axis: BESettings.AXIS_OPTIONS.speciesSex.id,
        y_axis: BESettings.AXIS_OPTIONS.system.id,
        filters: [
            BESettings.FILTER_OPTIONS.studyCitation.id,
            BESettings.FILTER_OPTIONS.experimentType.id,
            BESettings.FILTER_OPTIONS.generation.id,
        ],
        table_fields: [
            BESettings.TABLE_FIELDS.studyCitation.id,
            BESettings.TABLE_FIELDS.experimentName.id,
            BESettings.TABLE_FIELDS.animalGroupName.id,
            BESettings.TABLE_FIELDS.system.id,
            BESettings.TABLE_FIELDS.organ.id,
            BESettings.TABLE_FIELDS.effect.id,
            BESettings.TABLE_FIELDS.endpointName.id,
        ],
    },
    {
        id: "test subject vs. study design & system",
        label: "test subject vs. study design & system",
        upperColor: COLORS.red,
        x_axis: BESettings.AXIS_OPTIONS.speciesSex.id,
        y_axis: BESettings.AXIS_OPTIONS.experimentTypeSystem.id,
        filters: [
            BESettings.FILTER_OPTIONS.studyCitation.id,
            BESettings.FILTER_OPTIONS.generation.id,
            BESettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BESettings.TABLE_FIELDS.studyCitation.id,
            BESettings.TABLE_FIELDS.experimentName.id,
            BESettings.TABLE_FIELDS.animalGroupName.id,
            BESettings.TABLE_FIELDS.system.id,
            BESettings.TABLE_FIELDS.organ.id,
            BESettings.TABLE_FIELDS.effect.id,
            BESettings.TABLE_FIELDS.endpointName.id,
        ],
    },
    {
        id: "reference vs. system",
        label: "reference vs. system",
        upperColor: COLORS.green,
        x_axis: BESettings.AXIS_OPTIONS.studyCitation.id,
        y_axis: BESettings.AXIS_OPTIONS.system.id,
        filters: [],
        table_fields: [
            BESettings.TABLE_FIELDS.studyCitation.id,
            BESettings.TABLE_FIELDS.experimentName.id,
            BESettings.TABLE_FIELDS.animalGroupName.id,
            BESettings.TABLE_FIELDS.system.id,
            BESettings.TABLE_FIELDS.organ.id,
            BESettings.TABLE_FIELDS.effect.id,
            BESettings.TABLE_FIELDS.endpointName.id,
        ],
    },
    {
        id: "reference vs. study design & system",
        label: "reference vs. study design & system",
        upperColor: COLORS.purple,
        x_axis: BESettings.AXIS_OPTIONS.studyCitation.id,
        y_axis: BESettings.AXIS_OPTIONS.experimentTypeSystem.id,
        filters: [],
        table_fields: [
            BESettings.TABLE_FIELDS.studyCitation.id,
            BESettings.TABLE_FIELDS.experimentName.id,
            BESettings.TABLE_FIELDS.animalGroupName.id,
            BESettings.TABLE_FIELDS.system.id,
            BESettings.TABLE_FIELDS.organ.id,
            BESettings.TABLE_FIELDS.effect.id,
            BESettings.TABLE_FIELDS.endpointName.id,
        ],
    },
];

// BED = Bioassay endpoint doses
const BED = {
        studyId: defineProps("studyId", "Study id", "study id"),
        studyCitation: defineProps("studyCitation", "Study citation", "study citation"),
        studyIdentifier: defineProps("studyIdentifier", "Study identifier", "study identifier"),
        studyEval: defineProps("studyEval", "Overall study evaluation", "overall study evaluation"),
        experimentId: defineProps("experimentId", "Experiment id", "experiment id"),
        experimentName: defineProps("experimentName", "Experiment name", "experiment name"),
        experimentType: defineProps("experimentType", "Study design", "experiment type"),
        treatmentPeriod: defineProps("treatmentPeriod", "Treatment period", "treatment period"),
        experimentCas: defineProps("experimentCas", "Experiment CAS", "experiment cas"),
        chemical: defineProps("chemical", "Experiment chemical", "experiment chemical"),
        animalGroupId: defineProps("animalGroupId", "Animal group id", "animal group id"),
        animalGroupName: defineProps("animalGroupName", "Animal group name", "animal group name"),
        animalDesc: defineProps("animalDesc", "Animal description", "animal description"),
        animalDescN: defineProps(
            "animalDescN",
            "Animal description, with N",
            "animal description, with n"
        ),
        species: defineProps("species", "Species", "species"),
        strain: defineProps("strain", "Strain", "strain"),
        sex: defineProps("sex", "Sex", "sex"),
        generation: defineProps("generation", "Generation", "generation"),
        routeOfExposure: defineProps("routeOfExposure", "Route of exposure", "route of exposure"),
        endpointId: defineProps("endpointId", "Endpoint ID", "endpoint id"),
        system: defineProps("system", "System", "system"),
        organ: defineProps("organ", "Organ", "organ"),
        effect: defineProps("effect", "Effect", "effect"),
        effectSubtype: defineProps("effectSubtype", "Effect subtype", "effect subtype"),
        endpointName: defineProps("endpointName", "Endpoint name", "endpoint name"),
        diagnostic: defineProps("diagnostic", "Diagnostic", "diagnostic"),
        observationTime: defineProps("observationTime", "Observation time", "observation time"),
        doseUnitsId: defineProps("doseUnitsId", "Dose units ID", "dose units id"),
        doseUnitsName: defineProps("doseUnitsName", "Dose units name", "dose units name"),
        doses: defineProps("doses", "Doses", "doses"),
        noel: defineProps("noel", "NOEL", "noel"),
        loel: defineProps("loel", "LOEL", "loel"),
        fel: defineProps("fel", "FEL", "fel"),
        bmd: defineProps("bmd", "BMD", "bmd"),
        bmdl: defineProps("bmdl", "BMDL", "bmdl"),
    },
    BEDSettings = {
        AXIS_OPTIONS: {
            studyCitation: defineAxis(BED.studyCitation),
            studyEval: defineAxis(BED.studyEval),
            speciesSex: defineMultiAxis([BED.species, BED.sex], "speciesSex", "Species & Sex"),
            experimentType: defineAxis(BED.experimentType),
            system: defineAxis(BED.system),
            organ: defineAxis(BED.organ),
            systemOrgan: defineMultiAxis([BED.system, BED.organ], "systemOrgan", "System & organ"),
            experimentTypeSystem: defineMultiAxis(
                [BED.experimentType, BED.system],
                "experimentTypeSystem",
                "Study design & system"
            ),
            endpointName: defineAxis(BED.endpointName),
            diagnostic: defineAxis(BED.diagnostic),
        },
        FILTER_OPTIONS: {
            doseUnitsName: defineFilter(BED.doseUnitsName),
            studyCitation: defineFilter(BED.studyCitation, {on_click_event: "study"}),
            studyEval: defineFilter(BED.studyEval),
            experimentType: defineFilter(BED.experimentType),
            species: defineFilter(BED.species),
            strain: defineFilter(BED.strain),
            sex: defineFilter(BED.sex),
            system: defineFilter(BED.system),
            organ: defineFilter(BED.organ),
            effect: defineFilter(BED.effect, {on_click_event: "endpoint_complete"}),
            effectSubtype: defineFilter(BED.effectSubtype, {on_click_event: "endpoint_complete"}),
            endpointName: defineFilter(BED.endpointName),
            diagnostic: defineFilter(BED.diagnostic),
            observationTime: defineFilter(BED.observationTime),
        },
        TABLE_FIELDS: {
            studyCitation: defineTable(BED.studyCitation, {on_click_event: "study"}),
            studyEval: defineTable(BED.studyEval),
            experimentName: defineTable(BED.experimentName, {on_click_event: "experiment"}),
            treatmentPeriod: defineTable(BED.treatmentPeriod),
            animalGroupName: defineTable(BED.animalGroupName, {on_click_event: "animal_group"}),
            animalDesc: defineTable(BED.animalDesc, {on_click_event: "animal_group"}),
            animalDescN: defineTable(BED.animalDescN, {on_click_event: "animal_group"}),
            species: defineTable(BED.species),
            strain: defineTable(BED.strain),
            sex: defineTable(BED.sex),
            system: defineTable(BED.system),
            organ: defineTable(BED.organ),
            effect: defineTable(BED.effect),
            effectSubtype: defineTable(BED.effectSubtype),
            endpointName: defineTable(BED.endpointName, {on_click_event: "endpoint_complete"}),
            diagnostic: defineTable(BED.diagnostic),
            observationTime: defineTable(BED.observationTime),
            doses: defineTable(BED.doses),
            doseUnitsName: defineTable(BED.doseUnitsName),
            noel: defineTable(BED.noel),
            loel: defineTable(BED.loel),
            fel: defineTable(BED.fel),
            bmd: defineTable(BED.bmd),
            bmdl: defineTable(BED.bmdl),
        },
        DASHBOARDS: [],
    };

// define dashboards after building-blocks are defined
BEDSettings.DASHBOARDS = [
    {
        id: "study design vs. system",
        label: "study design vs. system",
        upperColor: COLORS.blue,
        x_axis: BEDSettings.AXIS_OPTIONS.experimentType.id,
        y_axis: BEDSettings.AXIS_OPTIONS.system.id,
        filters: [
            BEDSettings.FILTER_OPTIONS.doseUnitsName.id,
            BEDSettings.FILTER_OPTIONS.experimentType.id,
            BEDSettings.FILTER_OPTIONS.studyCitation.id,
            BEDSettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BEDSettings.TABLE_FIELDS.studyCitation.id,
            BEDSettings.TABLE_FIELDS.experimentName.id,
            BEDSettings.TABLE_FIELDS.animalGroupName.id,
            BEDSettings.TABLE_FIELDS.system.id,
            BEDSettings.TABLE_FIELDS.organ.id,
            BEDSettings.TABLE_FIELDS.effect.id,
            BEDSettings.TABLE_FIELDS.endpointName.id,
            BEDSettings.TABLE_FIELDS.doses.id,
            BEDSettings.TABLE_FIELDS.doseUnitsName.id,
            BEDSettings.TABLE_FIELDS.noel.id,
            BEDSettings.TABLE_FIELDS.loel.id,
            BEDSettings.TABLE_FIELDS.bmd.id,
            BEDSettings.TABLE_FIELDS.bmdl.id,
        ],
    },
    {
        id: "study design vs. test subject",
        label: "study design vs. test subject",
        upperColor: COLORS.black,
        x_axis: BEDSettings.AXIS_OPTIONS.experimentType.id,
        y_axis: BEDSettings.AXIS_OPTIONS.speciesSex.id,
        filters: [
            BEDSettings.FILTER_OPTIONS.doseUnitsName.id,
            BEDSettings.FILTER_OPTIONS.system.id,
        ],
        table_fields: [
            BEDSettings.TABLE_FIELDS.studyCitation.id,
            BEDSettings.TABLE_FIELDS.experimentName.id,
            BEDSettings.TABLE_FIELDS.animalGroupName.id,
            BEDSettings.TABLE_FIELDS.system.id,
            BEDSettings.TABLE_FIELDS.organ.id,
            BEDSettings.TABLE_FIELDS.effect.id,
            BEDSettings.TABLE_FIELDS.endpointName.id,
            BEDSettings.TABLE_FIELDS.doses.id,
            BEDSettings.TABLE_FIELDS.doseUnitsName.id,
            BEDSettings.TABLE_FIELDS.noel.id,
            BEDSettings.TABLE_FIELDS.loel.id,
            BEDSettings.TABLE_FIELDS.bmd.id,
            BEDSettings.TABLE_FIELDS.bmdl.id,
        ],
    },
    {
        id: "test subject vs. study design & system",
        label: "test subject vs. study design & system",
        upperColor: COLORS.orange,
        x_axis: BEDSettings.AXIS_OPTIONS.speciesSex.id,
        y_axis: BEDSettings.AXIS_OPTIONS.experimentTypeSystem.id,
        filters: [
            BEDSettings.FILTER_OPTIONS.doseUnitsName.id,
            BEDSettings.FILTER_OPTIONS.studyCitation.id,
            BEDSettings.FILTER_OPTIONS.organ.id,
            BEDSettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BEDSettings.TABLE_FIELDS.studyCitation.id,
            BEDSettings.TABLE_FIELDS.experimentName.id,
            BEDSettings.TABLE_FIELDS.animalGroupName.id,
            BEDSettings.TABLE_FIELDS.system.id,
            BEDSettings.TABLE_FIELDS.organ.id,
            BEDSettings.TABLE_FIELDS.effect.id,
            BEDSettings.TABLE_FIELDS.endpointName.id,
            BEDSettings.TABLE_FIELDS.doses.id,
            BEDSettings.TABLE_FIELDS.doseUnitsName.id,
            BEDSettings.TABLE_FIELDS.noel.id,
            BEDSettings.TABLE_FIELDS.loel.id,
            BEDSettings.TABLE_FIELDS.bmd.id,
            BEDSettings.TABLE_FIELDS.bmdl.id,
        ],
    },
    {
        id: "reference vs. system",
        label: "reference vs. system",
        upperColor: COLORS.green,
        x_axis: BEDSettings.AXIS_OPTIONS.studyCitation.id,
        y_axis: BEDSettings.AXIS_OPTIONS.system.id,
        filters: [
            BEDSettings.FILTER_OPTIONS.doseUnitsName.id,
            BEDSettings.FILTER_OPTIONS.effect.id,
        ],
        table_fields: [
            BEDSettings.TABLE_FIELDS.studyCitation.id,
            BEDSettings.TABLE_FIELDS.experimentName.id,
            BEDSettings.TABLE_FIELDS.animalGroupName.id,
            BEDSettings.TABLE_FIELDS.system.id,
            BEDSettings.TABLE_FIELDS.organ.id,
            BEDSettings.TABLE_FIELDS.effect.id,
            BEDSettings.TABLE_FIELDS.endpointName.id,
            BEDSettings.TABLE_FIELDS.doses.id,
            BEDSettings.TABLE_FIELDS.doseUnitsName.id,
            BEDSettings.TABLE_FIELDS.noel.id,
            BEDSettings.TABLE_FIELDS.loel.id,
            BEDSettings.TABLE_FIELDS.bmd.id,
            BEDSettings.TABLE_FIELDS.bmdl.id,
        ],
    },
    {
        id: "reference vs. study design & system",
        label: "reference vs. study design & system",
        upperColor: COLORS.purple,
        x_axis: BEDSettings.AXIS_OPTIONS.studyCitation.id,
        y_axis: BEDSettings.AXIS_OPTIONS.experimentTypeSystem.id,
        filters: [BEDSettings.FILTER_OPTIONS.doseUnitsName.id],
        table_fields: [
            BEDSettings.TABLE_FIELDS.studyCitation.id,
            BEDSettings.TABLE_FIELDS.experimentName.id,
            BEDSettings.TABLE_FIELDS.animalGroupName.id,
            BEDSettings.TABLE_FIELDS.system.id,
            BEDSettings.TABLE_FIELDS.organ.id,
            BEDSettings.TABLE_FIELDS.effect.id,
            BEDSettings.TABLE_FIELDS.endpointName.id,
            BEDSettings.TABLE_FIELDS.doses.id,
            BEDSettings.TABLE_FIELDS.doseUnitsName.id,
            BEDSettings.TABLE_FIELDS.noel.id,
            BEDSettings.TABLE_FIELDS.loel.id,
            BEDSettings.TABLE_FIELDS.bmd.id,
            BEDSettings.TABLE_FIELDS.bmdl.id,
        ],
    },
];

export {BEDSettings, BESettings, BSDSettings};

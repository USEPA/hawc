from django.db import models


class YesNoNr(models.TextChoices):
    YS = "YS", "Yes"
    NO = "NO", "No"
    NR = "NR", "Not reported"


class YesNoNs(models.TextChoices):
    YS = "YS", "yes"
    NO = "NO", "no"
    NS = "NS", "not specified"


class ExperimentType(models.TextChoices):
    ACU = "ACU", "acute"
    SHT = "SHT", "short-term"
    SCT = "SCT", "sub-chronic toxicity"
    CT = "CT", "chronic toxicity"
    CAN = "CAN", "cancer"
    DTR = "DTR", "developmental toxicity and repro"
    MUT = "MUT", "mutagenicity"
    NR = "NR", "not reported"
    OTH = "OTH", "other"


class DevelopmentalOrReproductiveToxicityType(models.TextChoices):
    RE = "RE", "Reproduction studies (one, two and multi-generational studies"
    DN = "DN", "Developmental neurotoxicity"
    DI = "DI", "Developmental immunotoxicity studies "
    PD = "PD", "Pubertal development "
    FR = "FR", "Female reproductive toxicity"
    EF = "EF", "Embryo-fetal development studies"
    PP = "PP", "Perinatal/postnatal development"


class TestSubstanceComposition(models.TextChoices):
    MET = "MET", "metabolite"
    MIX = "MIX", "mixture"
    MUL = "MUL", "multiple substances"
    FOR = "FOR", "formulation"
    PAR = "PAR", "parent"


class TestSubstancePurity(models.TextChoices):
    AN = "AN", "analytical grade"
    TE = "TE", "technical grade"
    NS = "NS", "purity not specified"
    NA = "NA", "not applicable (e.g. in silico study) "


class AnimalGroupGeneration(models.TextChoices):
    P0 = "P0", "P0"
    P1 = "P1", "P1"
    P2 = "P2", "P2"
    F0 = "F0", "F0"
    F1 = "F1", "F1"
    F2 = "F2", "F2"
    UN = "UN", "unknown/not reported"
    OT = "OT", "other"


class AnimalGroupCohortType(models.TextChoices):
    SAT = "SAT", "satellite"
    REC = "REC", "recovery"
    SEN = "SEN", "sentinel"
    INT = "INT", "interim"
    TER = "TER", "terminal"
    PM1 = "PM1", "post first mating"
    PM2 = "PM2", "post second mating"
    PM3 = "PM3", "post third mating"
    OTH = "OTH", "other"


class AnimalGroupSource(models.TextChoices):
    COM = "COM", "commercial supplier, specify"
    NON = "NON", "non-commercial supplier, specify"
    HOU = "HOU", "In-house developed, specify"
    OTH = "OTH", "other"


class AnimalGroupSex(models.TextChoices):
    M = "M", "Male"
    F = "F", "Female"
    MF = "MF", "Combined"
    NS = "NS", "not specified"


class HusbandryRandomization(models.TextChoices):
    YES = "YES", "yes, with remarks"
    NO = "NO", "no"
    OTH = "OTH", "other"
    UNK = "UNK", "unknown"


class HusbandryCageMaterial(models.TextChoices):
    GLA = "GLA", "glass"
    PCA = "PCA", "polycarbonate"
    PPR = "PPR", "polypropylene"
    PT = "PT", "Polyethylene terepthalate"
    SS = "SS", "stainless steel"
    ALU = "ALU", "aluminum"
    MSH = "MSH", "wire mesh"
    ACR = "ACR", "acrylic"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class HusbandryBeddingMaterial(models.TextChoices):
    WOO = "WOO", "wood shavings"
    PAP = "PAP", "paper"
    COB = "COB", "corn cob"
    HAY = "HAY", "hay or straw"
    COC = "COC", "coconut fibre (coir)"
    PEL = "PEL", "pelleted"
    FLC = "FLC", "fleece"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class HusbandryEnrichmentMaterial(models.TextChoices):
    SHE = "SHE", "structural (shelter/hiding place)"
    PLA = "PLA", "structural (platform or perch)"
    CLB = "CLB", "structural (branches or climbing structure)"
    TOY = "TOY", "manipulative (toys and objects)"
    FOR = "FOR", "manipulative (foraging devices)"
    CHW = "CHW", "manipulative (chewable items)"
    VIS = "VIS", "sensory (visual stimuli)"
    AUD = "AUD", "sensory (auditory stimuli)"
    OLF = "OLF", "sensory (olfactory stimuli)"
    ENV = "ENV", "environmental (natural materials)"
    PUZ = "PUZ", "cognitive (puzzle feeders)"
    TRA = "TRA", "cognitive (training and tasks)"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class HusbandryWaterBottleMaterial(models.TextChoices):
    GLA = "GLA", "glass"
    PCA = "PCA", "polycarbonate"
    PPR = "PPR", "polypropylene"
    PT = "PT", "Polyethylene terepthalate"
    SS = "SS", "stainless steel"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class HusbandryIdentification(models.TextChoices):
    EAN = "EAN", "ear notch"
    EAT = "EAT", "ear tag"
    CHP = "CHP", "microchip"
    TAT = "TAT", "tattoo"
    TOE = "TOE", "toe clipping"
    FRC = "FRC", "fur clipping"
    FRD = "FRD", "fur dyeing"
    COL = "COL", "collar or band"
    PAI = "PAI", "paint or marker"
    NAT = "NAT", "natural markings"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class HusbandryFeedingFrequency(models.TextChoices):
    ADL = "ADL", "ad libitum"
    OTH = "OTH", "other, specify"
    NS = "NS", "not specified"


class HusbandryDiet(models.TextChoices):
    CON = "CON", "conventional"
    RES = "RES", "calorie restricted"
    FAS = "FAS", "fasted"
    NS = "NS", "not specified"


class HusbandryWater(models.TextChoices):
    TAP = "TAP", "tap water"
    FIL = "FIL", "filtered water"
    DEI = "DEI", "deionized water"
    DIS = "DIS", "distilled water"
    RVO = "RVO", "reverse osmosis water"
    STR = "STR", "sterile water"
    ACI = "ACI", "acidified water"
    SUP = "SUP", "supplemented water"
    OTH = "OTH", "other"
    NS = "NS", "not specified"


class TreatmentRouteOfExposure(models.TextChoices):
    ORA = "ORA", "oral"
    SCU = "SCU", "subcutaneous"
    DER = "DER", "dermal"
    INH = "INH", "inhalation"
    INJ = "INJ", "injection"
    OCU = "OCU", "ocular"
    OTH = "OTH", "other, specify"


class TreatmentExposureMethod(models.TextChoices):
    ORCAP = "ORCAP", "oral capsule"
    ORDIE = "ORDIE", "oral diet"
    ORGAV = "ORGAV", "oral gavage"
    ORWAT = "ORWAT", "oral drinking water"
    INGAS = "INGAS", "inhalation - gas"
    INPAR = "INPAR", "inhalation - particle"
    INVAP = "INVAP", "inhalation - vapor"
    DERM = "DERM", "dermal"
    IJSUB = "IJSUB", "subcutaneous injection"
    IJPER = "IJPER", "intraperitoneal injection"
    IJIV = "IJIV", "intravenous injection"
    INOVO = "INOVO", "in ovo"
    PAREN = "PAREN", "parental"
    BODY = "BODY", "whole body"
    MULTI = "MULTI", "multiple"
    UNKWN = "UNKWN", "unknown"
    OTHER = "OTHER", "other"


class TreatmentLifestage(models.TextChoices):
    EMB = "EMB", "embryonic"
    FET = "FET", "fetal"
    NEO = "NEO", "neonate"
    JUV = "JUV", "juvenile"
    ADO = "ADO", "adolescent"
    ADU = "ADU", "adult"
    SEN = "SEN", "senior"
    NA = "NA", "NA"


class TreatmentAgeUnit(models.TextChoices):
    D = "D", "Day"
    DPM = "DPM", "day (premating)"
    DGE = "DGE", "GD (gestational day)"
    DPN = "DPN", "PND (post-natal day)"
    W = "W", "week"
    WPM = "WPM", "week (premating)"
    MON = "MON", "month"
    YEA = "YEA", "year"
    GEN = "GEN", "generation"

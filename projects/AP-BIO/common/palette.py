"""Role-based colours for the AP Biology chemistry-concepts track."""

# Ground and prose match the repository-wide visual system.
BG = "#0C0E12"
INK = "#EDF0F4"
MUTED = "#8A93A0"

# Atom colours describe their role in a diagram, not literal CPK elements.
ATOM_PRIMARY = "#4FA8E8"
ATOM_PARTNER = "#F0B429"
ATOM_CONTEXT = "#9D6FE0"

# Bonding roles remain stable even if the theme is changed later.
ELECTRON = "#EDF0F4"
BOND_COVALENT = "#EDF0F4"
BOND_IONIC = "#5FCF80"
BOND_WEAK = "#8A93A0"
CHARGE_POS = "#E8615A"
CHARGE_NEG = "#4FA8E8"

# Partial charges (dipoles) are a distinct concept from full ionic charge --
# same hue family as CHARGE_POS/CHARGE_NEG so the sign still reads instantly,
# muted so a delta badge never gets confused with a full +/- ionic badge.
DELTA_POS = "#D98883"
DELTA_NEG = "#7FB3D9"

# The coiled polypeptide backbone in the protein secondary-structure beat.
# Lighter than MUTED so the ribbon itself stays visible while dashed
# hydrogen-bond rungs (BOND_WEAK) still read as the secondary, fainter layer.
BACKBONE = "#C7CCD6"

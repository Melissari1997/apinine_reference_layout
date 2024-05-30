FWI_MIN = 0
FWI_MAX = 50
VULN_MIN = 0
VULN_MAX = 1
AAL_MIN = 0
AAL_MAX = 0.05
RISK_INDEX_MIN = 0
RISK_INDEX_MAX = 5

wildfire_layer_range = {
    "intensity_rp2": (FWI_MIN, FWI_MAX),
    "intensity_rp10": (FWI_MIN, FWI_MAX),
    "intensity_rp30": (FWI_MIN, FWI_MAX),
    "vulnerability_rp2": (VULN_MIN, VULN_MAX),
    "vulnerability_rp10": (VULN_MIN, VULN_MAX),
    "vulnerability_rp30": (VULN_MIN, VULN_MAX),
    "aal": (AAL_MIN, AAL_MAX),
    "risk_index": (RISK_INDEX_MIN, RISK_INDEX_MAX),
}
